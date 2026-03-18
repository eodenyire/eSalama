package com.esalama.gatescanner.data.api

import com.google.gson.GsonBuilder
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.util.concurrent.TimeUnit

/**
 * Retrofit client for API communication
 */
object RetrofitClient {
    
    private var retrofit: Retrofit? = null
    private var baseUrl: String = "http://10.0.2.2:8000/" // Default for Android emulator

    fun setBaseUrl(url: String) {
        var formattedUrl = url
        if (!formattedUrl.endsWith("/")) {
            formattedUrl += "/"
        }
        if (formattedUrl != baseUrl) {
            baseUrl = formattedUrl
            retrofit = null // Force recreation of retrofit instance
        }
    }

    fun getClient(): Retrofit {
        if (retrofit == null) {
            val loggingInterceptor = HttpLoggingInterceptor().apply {
                level = HttpLoggingInterceptor.Level.BODY
            }

            val client = OkHttpClient.Builder()
                .addInterceptor(loggingInterceptor)
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .build()

            val gson = GsonBuilder()
                .setLenient()
                .create()

            retrofit = Retrofit.Builder()
                .baseUrl(baseUrl)
                .client(client)
                .addConverterFactory(GsonConverterFactory.create(gson))
                .build()
        }
        return retrofit!!
    }

    fun getApiService(): ESalamaApiService {
        return getClient().create(ESalamaApiService::class.java)
    }
}
