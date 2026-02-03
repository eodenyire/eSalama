package com.esalama.gatescanner.ui

import android.annotation.SuppressLint
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.esalama.gatescanner.R
import com.esalama.gatescanner.data.api.RetrofitClient
import com.esalama.gatescanner.data.model.AttendanceRecord
import com.esalama.gatescanner.data.model.NotificationRequest
import com.esalama.gatescanner.data.model.QRValidationRequest
import com.esalama.gatescanner.utils.PreferencesManager
import com.google.mlkit.vision.barcode.BarcodeScanning
import com.google.mlkit.vision.barcode.common.Barcode
import com.google.mlkit.vision.common.InputImage
import kotlinx.coroutines.launch
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

/**
 * QR Scanner Activity using CameraX and ML Kit
 */
class QRScannerActivity : AppCompatActivity() {

    private lateinit var previewView: PreviewView
    private lateinit var resultTextView: TextView
    private lateinit var progressBar: ProgressBar
    private lateinit var prefsManager: PreferencesManager
    private lateinit var cameraExecutor: ExecutorService
    
    private var isProcessing = false
    private var lastScannedCode: String? = null
    private var lastScanTime: Long = 0

    companion object {
        private const val TAG = "QRScannerActivity"
        private const val SCAN_COOLDOWN_MS = 3000L // 3 seconds cooldown between scans
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_qr_scanner)

        prefsManager = PreferencesManager(this)

        // Initialize views
        previewView = findViewById(R.id.previewView)
        resultTextView = findViewById(R.id.resultTextView)
        progressBar = findViewById(R.id.progressBar)

        cameraExecutor = Executors.newSingleThreadExecutor()

        // Start camera
        startCamera()
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)

        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            // Preview
            val preview = Preview.Builder()
                .build()
                .also {
                    it.setSurfaceProvider(previewView.surfaceProvider)
                }

            // Image analysis for QR scanning
            val imageAnalyzer = ImageAnalysis.Builder()
                .setBackpressureStrategy(ImageAnalysis.STRATEGY_KEEP_ONLY_LATEST)
                .build()
                .also {
                    it.setAnalyzer(cameraExecutor, QRCodeAnalyzer())
                }

            // Select back camera
            val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA

            try {
                // Unbind use cases before rebinding
                cameraProvider.unbindAll()

                // Bind use cases to camera
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageAnalyzer
                )

            } catch (exc: Exception) {
                Log.e(TAG, "Use case binding failed", exc)
            }

        }, ContextCompat.getMainExecutor(this))
    }

    private inner class QRCodeAnalyzer : ImageAnalysis.Analyzer {
        private val scanner = BarcodeScanning.getClient()

        @SuppressLint("UnsafeOptInUsageError")
        override fun analyze(imageProxy: ImageProxy) {
            val mediaImage = imageProxy.image
            if (mediaImage != null && !isProcessing) {
                val image = InputImage.fromMediaImage(
                    mediaImage,
                    imageProxy.imageInfo.rotationDegrees
                )

                scanner.process(image)
                    .addOnSuccessListener { barcodes ->
                        for (barcode in barcodes) {
                            barcode.rawValue?.let { qrCode ->
                                handleQRCode(qrCode)
                            }
                        }
                    }
                    .addOnFailureListener {
                        Log.e(TAG, "Barcode scanning failed", it)
                    }
                    .addOnCompleteListener {
                        imageProxy.close()
                    }
            } else {
                imageProxy.close()
            }
        }
    }

    private fun handleQRCode(qrCode: String) {
        // Prevent duplicate scans
        val currentTime = System.currentTimeMillis()
        if (qrCode == lastScannedCode && (currentTime - lastScanTime) < SCAN_COOLDOWN_MS) {
            return
        }

        lastScannedCode = qrCode
        lastScanTime = currentTime
        isProcessing = true

        runOnUiThread {
            showLoading(true)
            resultTextView.text = "Processing QR code..."
        }

        // Validate and process QR code
        validateAndProcessQR(qrCode)
    }

    private fun validateAndProcessQR(qrToken: String) {
        lifecycleScope.launch {
            try {
                val apiService = RetrofitClient.getApiService()
                val token = prefsManager.getBearerToken()
                
                if (token == null) {
                    showError("Not authenticated. Please log in again.")
                    return@launch
                }

                // Validate QR code
                val validationRequest = QRValidationRequest(
                    qrToken = qrToken,
                    scannerId = prefsManager.getScannerId(),
                    location = "Main Gate"
                )

                val response = apiService.validateQR(validationRequest, token)

                if (response.isSuccessful && response.body() != null) {
                    val validationResponse = response.body()!!
                    
                    if (validationResponse.valid) {
                        // QR code is valid - record attendance
                        recordAttendance(validationResponse)
                    } else {
                        showError("Invalid QR code: ${validationResponse.message}")
                    }
                } else {
                    showError("Validation failed: ${response.message()}")
                }
            } catch (e: Exception) {
                showError("Error: ${e.message}")
                Log.e(TAG, "Error validating QR", e)
            } finally {
                isProcessing = false
                showLoading(false)
            }
        }
    }

    private suspend fun recordAttendance(validationResponse: com.esalama.gatescanner.data.model.QRValidationResponse) {
        try {
            val apiService = RetrofitClient.getApiService()
            val token = prefsManager.getBearerToken() ?: return

            // Get current timestamp
            val timestamp = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss", Locale.getDefault())
                .format(Date())

            // Create attendance record
            val attendanceRecord = AttendanceRecord(
                studentId = validationResponse.studentId ?: 0,
                scanType = validationResponse.scanType ?: "arrival",
                timestamp = timestamp,
                location = "Main Gate",
                scannerId = prefsManager.getScannerId()
            )

            // Record attendance
            val attendanceResponse = apiService.recordAttendance(attendanceRecord, token)

            if (attendanceResponse.isSuccessful) {
                // Send notifications to parent and teacher
                sendNotifications(validationResponse)
                
                // Show success message
                val message = """
                    ✓ SUCCESS
                    Student: ${validationResponse.studentName}
                    Class: ${validationResponse.studentClass}
                    Type: ${validationResponse.scanType?.uppercase()}
                    Time: ${SimpleDateFormat("HH:mm:ss", Locale.getDefault()).format(Date())}
                """.trimIndent()
                
                showSuccess(message)
            } else {
                showError("Failed to record attendance")
            }
        } catch (e: Exception) {
            showError("Error recording attendance: ${e.message}")
            Log.e(TAG, "Error recording attendance", e)
        }
    }

    private suspend fun sendNotifications(validationResponse: com.esalama.gatescanner.data.model.QRValidationResponse) {
        try {
            val apiService = RetrofitClient.getApiService()
            val token = prefsManager.getBearerToken() ?: return

            val notificationMessage = when (validationResponse.scanType) {
                "arrival" -> "Good morning, ${validationResponse.studentName} has safely entered the school gate at ${
                    SimpleDateFormat("hh:mm a", Locale.getDefault()).format(Date())
                }."
                "departure" -> "${validationResponse.studentName} has left the school at ${
                    SimpleDateFormat("hh:mm a", Locale.getDefault()).format(Date())
                }."
                else -> "${validationResponse.studentName} was scanned at the gate."
            }

            // Note: In a real implementation, you would get parent and teacher IDs from the backend
            // For now, we're creating a notification that the backend will route appropriately
            val notification = NotificationRequest(
                userId = validationResponse.studentId ?: 0,
                type = validationResponse.scanType ?: "arrival",
                message = notificationMessage,
                studentId = validationResponse.studentId
            )

            // Send notification (backend should handle routing to parents and teachers)
            apiService.sendNotification(notification, token)
            
            Log.d(TAG, "Notification sent successfully")
        } catch (e: Exception) {
            Log.e(TAG, "Error sending notifications", e)
            // Don't show error to user as this is not critical
        }
    }

    private fun showLoading(show: Boolean) {
        runOnUiThread {
            progressBar.visibility = if (show) View.VISIBLE else View.GONE
        }
    }

    private fun showSuccess(message: String) {
        runOnUiThread {
            resultTextView.text = message
            resultTextView.setTextColor(ContextCompat.getColor(this, android.R.color.holo_green_dark))
            Toast.makeText(this, "Attendance recorded successfully!", Toast.LENGTH_SHORT).show()
            
            // Reset after 3 seconds
            resultTextView.postDelayed({
                resultTextView.text = "Point camera at QR code"
                resultTextView.setTextColor(ContextCompat.getColor(this, android.R.color.white))
            }, 3000)
        }
    }

    private fun showError(message: String) {
        runOnUiThread {
            resultTextView.text = "ERROR: $message"
            resultTextView.setTextColor(ContextCompat.getColor(this, android.R.color.holo_red_dark))
            Toast.makeText(this, message, Toast.LENGTH_LONG).show()
            
            // Reset after 3 seconds
            resultTextView.postDelayed({
                resultTextView.text = "Point camera at QR code"
                resultTextView.setTextColor(ContextCompat.getColor(this, android.R.color.white))
            }, 3000)
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }
}
