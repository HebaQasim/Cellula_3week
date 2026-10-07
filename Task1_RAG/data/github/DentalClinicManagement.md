GitHub repository: DentalClinicManagement
Link: https://github.com/HebaQasim/DentalClinicManagement
Description: No description
Main language: C#

# 🦷 Dental Clinic Management API Documentation

This API provides endpoints for managing Admins, Customer Service users, Doctors, Treatments, and authentication in a dental clinic management system.

---

## 🔐 Authentication

### POST /api/auth/login
Authenticate user and return JWT token.

#### Request
```json
{
  "email": "user@example.com",
  "password": "string"
}
```

#### Response
```json
{
  "token": "jwt-token-value"
}
```

### POST /api/auth/forgot-password
Sends a reset link to user's email.

#### Request
```json
{
  "email": "user@example.com"
}
```

### POST /api/auth/reset-password
Resets the password using a valid token.

#### Request
```json
{
  "token": "reset-token",
  "newPassword": "string",
  "confirmPassword": "string"
}
```

---

## 👑 Admin

### GET /api/admin/profile
Retrieves current admin profile.

#### Response
```json
{
  "id": "guid",
  "fullName": "string",
  "email": "string",
  "phoneNumber": "string"
}
```

### PATCH /api/admin/{id}
Updates admin info.

#### Request
```json
{
  "fullName": "string",
  "email": "string",
  "phoneNumber": "string"
}
```

#### Response (Success)
```json
"Admin updated successfully"
```

#### Response (Success with Warning)
```json
{
  "message": "Admin updated successfully",
  "warning": "Warning message here"
}
```

### PATCH /api/admin/changePassword
Changes the admin's password.

#### Request
```json
{
  "currentPassword": "string",
  "newPassword": "string"
}
```

#### Response
```json
{
  "message": "Password changed successfully",
  "requireReLogin": true
}
```

---

## 👩‍💼 Customer Service

### POST /api/customerService
Adds a new customer service user. (Admin only)

#### Request
```json
{
  "fullName": "string",
  "workingTime": "string",
  "email": "string",
  "phoneNumber": "string"
}
```

#### Response
```json
{
  "customerServiceId": "guid"
}
```

### GET /api/customerService
Retrieves all customer service users.

#### Response
```json
[
  {
    "id": "guid",
    "fullName": "string",
    "workingTime": "string",
    "email": "string",
    "phoneNumber": "string",
    "isActive": true
  }
]
```

### GET /api/customerService/{id}
Gets details for a specific customer service user.

#### Response
```json
{
  "id": "guid",
  "fullName": "string",
  "workingTime": "string",
  "email": "string",
  "phoneNumber": "string",
  "isActive": true
}
```

### PATCH /api/customerService/{id}
Updates a customer service user.

#### Request
```json
{
  "fullName": "string",
  "workingTime": "string",
  "email": "string",
  "phoneNumber": "string",
  "isActive": true
}
```

#### Response
```json
"Customer Service updated successfully"
```

### PATCH /api/customerService/changePassword
Changes password (CustomerService role only).

#### Request
```json
{
  "currentPassword": "string",
  "newPassword": "string"
}
```

---

## 👨‍⚕️ Doctor

### POST /api/doctor
Adds a new doctor. (Admin only)

#### Request
```json
{
  "fullName": "string",
  "workingTime": "string",
  "email": "string",
  "phoneNumber": "string",
  "specialization": "string",
  "colorCode": "#RRGGBB"
}
```

#### Response
```json
{
  "doctorId": "guid"
}
```

### GET /api/doctor
Retrieves all doctors.

#### Response
```json
[
  {
    "id": "guid",
    "fullName": "string",
    "workingTime": "string",
    "email": "string",
    "phoneNumber": "string",
    "specialization": "string",
    "isActive": true,
    "colorCode": "#RRGGBB"
  }
]
```

### GET /api/doctor/{id}
Retrieves details for a doctor by ID.

#### Response
```json
{
  "id": "guid",
  "fullName": "string",
  "workingTime": "string",
  "email": "string",
  "phoneNumber": "string",
  "specialization": "string",
  "isActive": true,
  "colorCode": "#RRGGBB"
}
```

### PATCH /api/doctor/{id}
Updates a doctor's details.

### PATCH /api/doctor/changePassword
Doctor changes their password.

#### Request
```json
{
  "currentPassword": "string",
  "newPassword": "string"
}
```

### GET /api/doctor/search?name=...&phoneNumber=...
Searches for doctors by name or phone number.

### GET /api/doctor/filter?specialization=...
Filters doctors by specialization.

---

## 💼 Treatment

### POST /api/treatment
Adds a new treatment. (Admin only)

#### Request
```json
{
  "name": "string",
  "price": 0,
  "category": "string"
}
```

#### Response
```json
{
  "treatmentId": "guid"
}
```

### GET /api/treatment
Retrieves all treatments.

#### Response
```json
[
  {
    "id": "guid",
    "name": "string",
    "category": "string"
  }
]
```

### GET /api/treatment/{id}
Retrieves treatment details by ID.

#### Response
```json
{
  "id": "guid",
  "name": "string",
  "category": "string"
}
```

### PATCH /api/treatment/{id}
Updates a treatment.

#### Request
```json
{
  "name": "string",
  "category": "string",
  "price": 0
}
```

### DELETE /api/treatment/{id}
Deletes a treatment.

### GET /api/treatment/search?name=...
Searches for treatments by name.

### GET /api/treatment/filter?category=...&price=...
Filters treatments by category and/or price.
