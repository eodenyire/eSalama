package com.esalama.gatescanner.ui

import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.esalama.gatescanner.R
import com.esalama.gatescanner.data.api.RetrofitClient
import com.esalama.gatescanner.utils.PreferencesManager

/**
 * Settings activity for configuring API URL and scanner ID
 */
class SettingsActivity : AppCompatActivity() {

    private lateinit var apiUrlEditText: EditText
    private lateinit var scannerIdEditText: EditText
    private lateinit var saveButton: Button
    private lateinit var prefsManager: PreferencesManager

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_settings)

        // Enable back button
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        prefsManager = PreferencesManager(this)

        // Initialize views
        apiUrlEditText = findViewById(R.id.apiUrlEditText)
        scannerIdEditText = findViewById(R.id.scannerIdEditText)
        saveButton = findViewById(R.id.saveButton)

        // Load current settings
        apiUrlEditText.setText(prefsManager.getApiBaseUrl())
        scannerIdEditText.setText(prefsManager.getScannerId())

        saveButton.setOnClickListener {
            saveSettings()
        }
    }

    private fun saveSettings() {
        val apiUrl = apiUrlEditText.text.toString().trim()
        val scannerId = scannerIdEditText.text.toString().trim()

        if (apiUrl.isEmpty()) {
            apiUrlEditText.error = "API URL is required"
            return
        }

        if (scannerId.isEmpty()) {
            scannerIdEditText.error = "Scanner ID is required"
            return
        }

        // Validate URL format
        if (!apiUrl.startsWith("http://") && !apiUrl.startsWith("https://")) {
            apiUrlEditText.error = "URL must start with http:// or https://"
            return
        }

        // Save settings
        prefsManager.setApiBaseUrl(apiUrl)
        prefsManager.setScannerId(scannerId)
        
        // Update Retrofit client
        RetrofitClient.setBaseUrl(apiUrl)

        Toast.makeText(this, "Settings saved successfully", Toast.LENGTH_SHORT).show()
        finish()
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }
}
