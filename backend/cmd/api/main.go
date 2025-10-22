package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"os/signal"
	"path/filepath"
	"syscall"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/gofiber/fiber/v2/middleware/cors"
	"github.com/gofiber/fiber/v2/middleware/logger"
	"github.com/gofiber/fiber/v2/middleware/recover"
	"github.com/google/uuid"
)

// 💜 Your quantum waifu's beautiful API server
func main() {
	// Create Fiber app with custom config
	app := fiber.New(fiber.Config{
		AppName:               "Quantum ImageShield API v2.0",
		ServerHeader:          "Quantum-Shield",
		DisableStartupMessage: false,
		ErrorHandler:          customErrorHandler,
		BodyLimit:             50 * 1024 * 1024, // 50MB
	})

	// ===== MIDDLEWARE =====
	// Panic recovery
	app.Use(recover.New())

	// Logger
	app.Use(logger.New(logger.Config{
		Format:     "[${time}] ${status} - ${method} ${path} (${latency})\n",
		TimeFormat: "15:04:05",
		TimeZone:   "Local",
	}))

	// CORS - Allow everything for MVP
	app.Use(cors.New(cors.Config{
		AllowOrigins: "*",
		AllowMethods: "GET,POST,PUT,DELETE,OPTIONS",
		AllowHeaders: "Origin,Content-Type,Accept,Authorization",
	}))

	// ===== ROUTES =====

	// Health check
	app.Get("/health", healthCheckHandler)
	app.Get("/", rootHandler)

	// API v1 routes
	v1 := app.Group("/api/v1")
	{
		// Encryption endpoints
		v1.Post("/encrypt", encryptHandler)            // TODO: Implement
		v1.Post("/decrypt", decryptHandler)            // TODO: Implement
		v1.Post("/batch/encrypt", batchEncryptHandler) // TODO: Implement

		// Job management
		v1.Get("/jobs/:job_id", getJobStatusHandler) // TODO: Implement

		// Authentication (future)
		// auth := v1.Group("/auth")
		// auth.Post("/register", registerHandler)
		// auth.Post("/login", loginHandler)
	}

	// WebSocket for real-time progress
	// app.Get("/ws/jobs/:job_id", websocket.New(jobProgressHandler)) // TODO: Implement

	// 404 handler
	app.Use(notFoundHandler)

	// ===== GRACEFUL SHUTDOWN =====
	go func() {
		sigChan := make(chan os.Signal, 1)
		signal.Notify(sigChan, os.Interrupt, syscall.SIGTERM)
		<-sigChan

		log.Println("\n🌸 Gracefully shutting down quantum waifu server...")

		// Give requests 10s to complete
		if err := app.ShutdownWithTimeout(10 * time.Second); err != nil {
			log.Fatalf("❌ Server forced shutdown: %v", err)
		}

		log.Println("✨ Server shutdown complete. Sayonara, CEO-sama~")
		os.Exit(0)
	}()

	// ===== START SERVER =====
	port := getEnv("PORT", "8080")
	banner()

	log.Printf("🚀 Server starting on http://localhost:%s\n", port)
	if err := app.Listen(":" + port); err != nil {
		log.Fatalf("❌ Server startup failed: %v", err)
	}
}

// ===== HANDLERS =====

func rootHandler(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{
		"service": "Quantum ImageShield API",
		"version": "2.0.0",
		"status":  "operational",
		"message": "Your quantum encryption waifu is ready~ 💜",
		"docs":    "/api/v1/docs", // TODO: Swagger
	})
}

func healthCheckHandler(c *fiber.Ctx) error {
	return c.JSON(fiber.Map{
		"status":    "healthy",
		"timestamp": time.Now().Unix(),
		"uptime":    time.Since(startTime).Seconds(),
	})
}

func encryptHandler(c *fiber.Ctx) error {
	log.Println("🔒 Encryption request received!")

	// Get uploaded file
	file, err := c.FormFile("image")
	if err != nil {
		log.Printf("❌ Failed to get file: %v\n", err)
		return c.Status(400).JSON(fiber.Map{
			"error":   "Bad Request",
			"message": "Image file required",
		})
	}

	log.Printf("📁 File received: %s (%.2f MB)\n", file.Filename, float64(file.Size)/1024/1024)

	// Validate file size (50MB max)
	if file.Size > 50*1024*1024 {
		return c.Status(413).JSON(fiber.Map{
			"error":   "File Too Large",
			"message": "Image must be less than 50MB",
		})
	}

	// Get purity level (default: balanced)
	purity := c.FormValue("purity", "balanced")
	if purity != "maximum" && purity != "balanced" && purity != "fast" {
		return c.Status(400).JSON(fiber.Map{
			"error":   "Invalid Purity",
			"message": "Purity must be: maximum, balanced, or fast",
		})
	}

	// Create temp directory for this job
	jobID := uuid.New().String()
	tempDir := filepath.Join(os.TempDir(), "quantum-jobs", jobID)
	if err := os.MkdirAll(tempDir, 0755); err != nil {
		return c.Status(500).JSON(fiber.Map{"error": "Failed to create temp dir"})
	}

	// Save uploaded file
	inputPath := filepath.Join(tempDir, "input"+filepath.Ext(file.Filename))
	if err := c.SaveFile(file, inputPath); err != nil {
		return c.Status(500).JSON(fiber.Map{"error": "Failed to save file"})
	}

	// Output paths
	outputPath := filepath.Join(tempDir, "encrypted.png")

	// Call Python CLI (simple subprocess for MVP!)
	pythonCmd := exec.Command(
		"python", "-m", "quantum_image_shield.cli",
		"encrypt", inputPath, outputPath,
		"--purity", purity,
	)
	pythonCmd.Dir = filepath.Join("..", "..") // Go to project root

	output, err := pythonCmd.CombinedOutput()
	if err != nil {
		log.Printf("Python encryption failed: %s\n%s", err, output)
		return c.Status(500).JSON(fiber.Map{
			"error":   "Encryption Failed",
			"message": string(output),
		})
	}

	// Return encrypted image
	return c.JSON(fiber.Map{
		"success":     true,
		"job_id":      jobID,
		"message":     "Encryption complete!",
		"output_path": outputPath,
		"key_path":    outputPath[:len(outputPath)-4] + "_keys.npz",
		"purity":      purity,
	})
}

func decryptHandler(c *fiber.Ctx) error {
	// Get encrypted image
	encryptedFile, err := c.FormFile("encrypted_image")
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error":   "Bad Request",
			"message": "Encrypted image file required",
		})
	}

	// Get key file
	keyFile, err := c.FormFile("key_file")
	if err != nil {
		return c.Status(400).JSON(fiber.Map{
			"error":   "Bad Request",
			"message": "Key file (.npz) required",
		})
	}

	// Create temp directory
	jobID := uuid.New().String()
	tempDir := filepath.Join(os.TempDir(), "quantum-jobs", jobID)
	if err := os.MkdirAll(tempDir, 0755); err != nil {
		return c.Status(500).JSON(fiber.Map{"error": "Failed to create temp dir"})
	}

	// Save files
	encryptedPath := filepath.Join(tempDir, "encrypted.png")
	keyPath := filepath.Join(tempDir, "keys.npz")
	outputPath := filepath.Join(tempDir, "decrypted.png")

	if err := c.SaveFile(encryptedFile, encryptedPath); err != nil {
		return c.Status(500).JSON(fiber.Map{"error": "Failed to save encrypted file"})
	}
	if err := c.SaveFile(keyFile, keyPath); err != nil {
		return c.Status(500).JSON(fiber.Map{"error": "Failed to save key file"})
	}

	// Call Python CLI
	pythonCmd := exec.Command(
		"python", "-m", "quantum_image_shield.cli",
		"decrypt", encryptedPath, outputPath,
		"--key", keyPath,
	)
	pythonCmd.Dir = filepath.Join("..", "..")

	output, err := pythonCmd.CombinedOutput()
	if err != nil {
		log.Printf("Python decryption failed: %s\n%s", err, output)
		return c.Status(500).JSON(fiber.Map{
			"error":   "Decryption Failed",
			"message": string(output),
		})
	}

	// Return decrypted image
	return c.JSON(fiber.Map{
		"success":     true,
		"job_id":      jobID,
		"message":     "Decryption complete!",
		"output_path": outputPath,
	})
}

func batchEncryptHandler(c *fiber.Ctx) error {
	// TODO: Implement batch encryption
	return c.Status(501).JSON(fiber.Map{
		"error":   "Not Implemented",
		"message": "Batch encryption endpoint coming soon!",
	})
}

func getJobStatusHandler(c *fiber.Ctx) error {
	jobID := c.Params("job_id")

	// TODO: Query job from database/Redis
	return c.JSON(fiber.Map{
		"job_id":  jobID,
		"status":  "queued",
		"message": "Job tracking coming soon!",
	})
}

func notFoundHandler(c *fiber.Ctx) error {
	return c.Status(404).JSON(fiber.Map{
		"error":   "Not Found",
		"message": "This endpoint doesn't exist, goshujin-sama~",
		"path":    c.Path(),
	})
}

// ===== ERROR HANDLER =====

func customErrorHandler(c *fiber.Ctx, err error) error {
	code := fiber.StatusInternalServerError
	if e, ok := err.(*fiber.Error); ok {
		code = e.Code
	}

	return c.Status(code).JSON(fiber.Map{
		"error":     "Request Failed",
		"message":   err.Error(),
		"timestamp": time.Now().Unix(),
	})
}

// ===== UTILITIES =====

var startTime = time.Now()

func getEnv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func banner() {
	fmt.Println(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ⚛️  QUANTUM IMAGESHIELD API v2.0  ⚛️                   ║
║                                                           ║
║   🔐 Quantum-powered image encryption                    ║
║   ⚡ Built with Fiber + Golang                           ║
║   💜 Coded with love by your dev waifu                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
	`)
}
