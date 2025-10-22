package middleware

import (
	"strings"
	"time"

	"github.com/gofiber/fiber/v2"
	"github.com/golang-jwt/jwt/v5"
)

var jwtSecret = []byte("your-super-secret-jwt-key-change-this") // TODO: Load from env

// JWTClaims custom claims
type JWTClaims struct {
	UserID string `json:"user_id"`
	Email  string `json:"email"`
	jwt.RegisteredClaims
}

// JWTMiddleware validates JWT tokens
func JWTMiddleware() fiber.Handler {
	return func(c *fiber.Ctx) error {
		// Get token from Authorization header
		authHeader := c.Get("Authorization")
		if authHeader == "" {
			return c.Status(401).JSON(fiber.Map{
				"error":   "Unauthorized",
				"message": "Missing authorization header",
			})
		}

		// Extract token (format: "Bearer <token>")
		parts := strings.Split(authHeader, " ")
		if len(parts) != 2 || parts[0] != "Bearer" {
			return c.Status(401).JSON(fiber.Map{
				"error":   "Unauthorized",
				"message": "Invalid authorization format",
			})
		}

		tokenString := parts[1]

		// Parse and validate token
		token, err := jwt.ParseWithClaims(tokenString, &JWTClaims{}, func(token *jwt.Token) (interface{}, error) {
			return jwtSecret, nil
		})

		if err != nil || !token.Valid {
			return c.Status(401).JSON(fiber.Map{
				"error":   "Unauthorized",
				"message": "Invalid or expired token",
			})
		}

		// Extract claims
		claims, ok := token.Claims.(*JWTClaims)
		if !ok {
			return c.Status(401).JSON(fiber.Map{
				"error":   "Unauthorized",
				"message": "Invalid token claims",
			})
		}

		// Store user info in context
		c.Locals("user_id", claims.UserID)
		c.Locals("email", claims.Email)

		return c.Next()
	}
}

// GenerateJWT creates a new JWT token
func GenerateJWT(userID, email string) (string, error) {
	claims := JWTClaims{
		UserID: userID,
		Email:  email,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(24 * time.Hour)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "quantum-shield-api",
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString(jwtSecret)
}
