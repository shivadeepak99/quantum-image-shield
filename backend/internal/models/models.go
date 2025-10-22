package models

import (
	"time"

	"github.com/google/uuid"
	"gorm.io/gorm"
)

// 💜 Job represents an encryption/decryption task
type Job struct {
	ID          uuid.UUID      `gorm:"type:uuid;primary_key" json:"id"`
	UserID      *uuid.UUID     `gorm:"type:uuid;index" json:"user_id,omitempty"` // Nullable for now (no auth yet)
	Type        JobType        `gorm:"type:varchar(20);not null" json:"type"`
	Status      JobStatus      `gorm:"type:varchar(20);not null;index" json:"status"`
	Progress    int            `gorm:"default:0" json:"progress"` // 0-100
	PurityLevel string         `gorm:"type:varchar(20)" json:"purity_level,omitempty"`
	
	// File references
	InputFileURL   string  `gorm:"type:text" json:"input_file_url"`
	OutputFileURL  string  `gorm:"type:text" json:"output_file_url,omitempty"`
	KeyFileURL     string  `gorm:"type:text" json:"key_file_url,omitempty"`
	
	// Metadata
	Metadata       JSONB   `gorm:"type:jsonb" json:"metadata,omitempty"`
	ErrorMessage   string  `gorm:"type:text" json:"error_message,omitempty"`
	
	// Timestamps
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

// JobType enum
type JobType string

const (
	JobTypeEncrypt JobType = "encrypt"
	JobTypeDecrypt JobType = "decrypt"
)

// JobStatus enum
type JobStatus string

const (
	JobStatusQueued     JobStatus = "queued"
	JobStatusProcessing JobStatus = "processing"
	JobStatusCompleted  JobStatus = "completed"
	JobStatusFailed     JobStatus = "failed"
)

// BeforeCreate hook to generate UUID
func (j *Job) BeforeCreate(tx *gorm.DB) error {
	if j.ID == uuid.Nil {
		j.ID = uuid.New()
	}
	return nil
}

// JSONB type for metadata
type JSONB map[string]interface{}

// ===== USER MODEL (Future Auth) =====

type User struct {
	ID            uuid.UUID      `gorm:"type:uuid;primary_key" json:"id"`
	Email         string         `gorm:"type:varchar(255);unique;not null" json:"email"`
	PasswordHash  string         `gorm:"type:varchar(255);not null" json:"-"`
	APIKey        string         `gorm:"type:varchar(64);unique;index" json:"api_key,omitempty"`
	SubscriptionTier string      `gorm:"type:varchar(20);default:'free'" json:"subscription_tier"`
	
	// Usage limits
	MonthlyQuota  int            `gorm:"default:100" json:"monthly_quota"`
	UsedQuota     int            `gorm:"default:0" json:"used_quota"`
	
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
	
	// Relations
	Jobs []Job `gorm:"foreignKey:UserID" json:"-"`
}

func (u *User) BeforeCreate(tx *gorm.DB) error {
	if u.ID == uuid.Nil {
		u.ID = uuid.New()
	}
	return nil
}

// ===== KEY STORAGE MODEL =====

type EncryptionKey struct {
	ID        uuid.UUID      `gorm:"type:uuid;primary_key" json:"id"`
	JobID     uuid.UUID      `gorm:"type:uuid;unique;not null;index" json:"job_id"`
	UserID    *uuid.UUID     `gorm:"type:uuid;index" json:"user_id,omitempty"`
	
	// Encrypted key data (stored as base64)
	KeyDataEncrypted string `gorm:"type:text;not null" json:"-"`
	Salt             string `gorm:"type:varchar(64)" json:"-"`
	
	ExpiresAt *time.Time     `json:"expires_at,omitempty"`
	CreatedAt time.Time      `json:"created_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

func (k *EncryptionKey) BeforeCreate(tx *gorm.DB) error {
	if k.ID == uuid.Nil {
		k.ID = uuid.New()
	}
	return nil
}
