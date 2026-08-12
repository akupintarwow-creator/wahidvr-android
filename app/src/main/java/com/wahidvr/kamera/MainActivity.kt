package com.wahidvr.kamera

import android.Manifest
import android.content.ContentValues
import android.content.pm.PackageManager
import android.graphics.*
import android.os.Build
import android.os.Bundle
import android.provider.MediaStore
import android.view.View
import android.view.WindowManager
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.camera.core.*
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import java.text.SimpleDateFormat
import java.util.*
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class MainActivity : AppCompatActivity() {

    private lateinit var viewFinder: PreviewView
    private lateinit var effectInfo: TextView
    private lateinit var captureBtn: ImageButton
    private lateinit var switchBtn: ImageButton
    private lateinit var clearBtn: ImageButton
    private lateinit var effectList: LinearLayout
    private lateinit var scrollEffects: ScrollView
    private lateinit var searchBox: EditText
    private lateinit var categorySpinner: Spinner

    private var imageCapture: ImageCapture? = null
    private lateinit var cameraExecutor: ExecutorService
    private var lensFacing = CameraSelector.LENS_FACING_BACK
    private var currentEffect = ""
    private var currentEffectId = ""
    private val effectManager = EffectManager()
    private var allEffectButtons = mutableListOf<Button>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)

        viewFinder = findViewById(R.id.viewFinder)
        effectInfo = findViewById(R.id.effectInfo)
        captureBtn = findViewById(R.id.captureBtn)
        switchBtn = findViewById(R.id.switchBtn)
        clearBtn = findViewById(R.id.clearBtn)
        effectList = findViewById(R.id.effectList)
        scrollEffects = findViewById(R.id.scrollEffects)
        searchBox = findViewById(R.id.searchBox)
        categorySpinner = findViewById(R.id.categorySpinner)

        cameraExecutor = Executors.newSingleThreadExecutor()

        setupCategories()
        setupEffectButtons()
        setupControls()
        setupSearch()

        if (allPermissionsGranted()) {
            startCamera()
        } else {
            ActivityCompat.requestPermissions(this, REQUIRED_PERMISSIONS, REQUEST_CODE_PERMISSIONS)
        }
    }

    private fun setupCategories() {
        val categories = mutableListOf("Semua Efek")
        categories.addAll(effectManager.getCategories())
        val adapter = ArrayAdapter(this, android.R.layout.simple_spinner_item, categories)
        adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
        categorySpinner.adapter = adapter
        categorySpinner.onItemSelectedListener = object : AdapterView.OnItemSelectedListener {
            override fun onItemSelected(parent: AdapterView<*>?, view: View?, position: Int, id: Long) {
                val category = categories[position]
                filterByCategory(category)
            }
            override fun onNothingSelected(parent: AdapterView<*>?) {}
        }
    }

    private fun filterByCategory(category: String) {
        effectList.removeAllViews()
        allEffectButtons.clear()
        val effects = if (category == "Semua Efek") {
            effectManager.effects
        } else {
            effectManager.getEffectsByCategory(category)
        }
        effects.forEach { effect ->
            addEffectButton(effect)
        }
    }

    private fun setupEffectButtons() {
        filterByCategory("Semua Efek")
    }

    private fun addEffectButton(effect: EffectManager.Effect) {
        val btn = Button(this).apply {
            text = effect.name
            setTextColor(Color.WHITE)
            setBackgroundColor(effect.color)
            val params = LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                100
            )
            params.setMargins(4, 2, 4, 2)
            layoutParams = params
            textSize = 11f
            setPadding(12, 6, 12, 6)
            tag = effect.id

            setOnClickListener {
                currentEffect = effect.name
                currentEffectId = effect.id
                effectInfo.text = effect.name
                effectInfo.setTextColor(effect.color)
                updateEffectSelection(this)
                applyEffectToPreview(effect.id)
            }
        }
        allEffectButtons.add(btn)
        effectList.addView(btn)
    }

    private fun updateEffectSelection(selectedBtn: Button) {
        allEffectButtons.forEach { btn ->
            btn.alpha = if (btn == selectedBtn) 1.0f else 0.6f
            btn.textSize = if (btn == selectedBtn) 13f else 11f
        }
    }

    private fun setupSearch() {
        searchBox.setOnFocusChangeListener { _, hasFocus ->
            if (hasFocus) {
                searchBox.hint = "Ketik nama efek..."
            } else {
                searchBox.hint = "Cari Efek..."
            }
        }

        searchBox.addTextChangedListener(object : android.text.TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {
                filterEffects(s.toString())
            }
            override fun afterTextChanged(s: android.text.Editable?) {}
        })
    }

    private fun filterEffects(query: String) {
        effectList.removeAllViews()
        allEffectButtons.clear()
        val filteredEffects = if (query.isEmpty()) {
            effectManager.effects
        } else {
            effectManager.effects.filter {
                it.name.contains(query, ignoreCase = true) ||
                it.category.contains(query, ignoreCase = true) ||
                it.id.contains(query, ignoreCase = true)
            }
        }
        filteredEffects.forEach { effect ->
            addEffectButton(effect)
        }
    }

    private fun setupControls() {
        captureBtn.setOnClickListener { takePhoto() }
        switchBtn.setOnClickListener { flipCamera() }
        clearBtn.setOnClickListener {
            currentEffect = ""
            currentEffectId = ""
            effectInfo.text = "Original"
            effectInfo.setTextColor(Color.parseColor("#00D4FF"))
            allEffectButtons.forEach { it.alpha = 1.0f }
            startCamera()
        }
    }

    private fun applyEffectToPreview(effectId: String) {
        // Apply effect to camera preview
        startCamera()
    }

    private fun startCamera() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraProviderFuture.addListener({
            val cameraProvider = cameraProviderFuture.get()

            val preview = Preview.Builder()
                .build()
                .also { it.setSurfaceProvider(viewFinder.surfaceProvider) }

            imageCapture = ImageCapture.Builder()
                .setCaptureMode(ImageCapture.CAPTURE_MODE_MINIMIZE_LATENCY)
                .build()

            val cameraSelector = CameraSelector.Builder()
                .requireLensFacing(lensFacing)
                .build()

            try {
                cameraProvider.unbindAll()
                cameraProvider.bindToLifecycle(
                    this, cameraSelector, preview, imageCapture
                )
            } catch (exc: Exception) {
                Toast.makeText(this, "Error: ${exc.message}", Toast.LENGTH_SHORT).show()
            }
        }, ContextCompat.getMainExecutor(this))
    }

    private fun takePhoto() {
        val imageCapture = imageCapture ?: return

        val name = SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(System.currentTimeMillis())
        val contentValues = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, name)
            put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg")
            if (Build.VERSION.SDK_INT > Build.VERSION_CODES.P) {
                put(MediaStore.Images.Media.RELATIVE_PATH, "Pictures/WahidVR")
            }
        }

        val outputOptions = ImageCapture.OutputFileOptions
            .Builder(contentResolver, MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
            .build()

        imageCapture.takePicture(
            outputOptions, ContextCompat.getMainExecutor(this),
            object : ImageCapture.OnImageSavedCallback {
                override fun onError(exc: ImageCaptureException) {
                    Toast.makeText(baseContext, "Error: ${exc.message}", Toast.LENGTH_SHORT).show()
                }

                override fun onImageSaved(output: ImageCapture.OutputFileResults) {
                    Toast.makeText(baseContext, "Foto tersimpan dengan efek: $currentEffect", Toast.LENGTH_SHORT).show()
                }
            }
        )
    }

    private fun flipCamera() {
        lensFacing = if (lensFacing == CameraSelector.LENS_FACING_BACK) {
            CameraSelector.LENS_FACING_FRONT
        } else {
            CameraSelector.LENS_FACING_BACK
        }
        startCamera()
    }

    private fun allPermissionsGranted() = REQUIRED_PERMISSIONS.all {
        ContextCompat.checkSelfPermission(baseContext, it) == PackageManager.PERMISSION_GRANTED
    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == REQUEST_CODE_PERMISSIONS) {
            if (allPermissionsGranted()) {
                startCamera()
            } else {
                Toast.makeText(this, "Izin kamera tidak diberikan!", Toast.LENGTH_SHORT).show()
                finish()
            }
        }
    }

    override fun onDestroy() {
        super.onDestroy()
        cameraExecutor.shutdown()
    }

    companion object {
        private const val REQUEST_CODE_PERMISSIONS = 10
        private val REQUIRED_PERMISSIONS = arrayOf(Manifest.permission.CAMERA)
    }
}
