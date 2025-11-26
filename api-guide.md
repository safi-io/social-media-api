# Backend API Guide for Linkup Social Media Platform

This document outlines all API endpoints, request/response structures, and data requirements for the Linkup frontend application.

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [User Profile Endpoints](#user-profile-endpoints)
3. [Posts Endpoints](#posts-endpoints)
4. [Projects Endpoints](#projects-endpoints)
5. [Social Interactions](#social-interactions)
6. [General Notes](#general-notes)

---

## Authentication Endpoints

### 1. User Registration (Signup)
**Endpoint:** `POST /api/auth/signup`

**Request Body:**
```json
{
  "fullName": "string (required, min 2 characters)",
  "email": "string (required, valid email format)",
  "password": "string (required, min 8 characters, must contain uppercase, lowercase, number, and special character)"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Account created successfully",
  "data": {
    "user": {
      "id": "string",
      "fullName": "string",
      "email": "string",
      "username": "string (auto-generated or from fullName)",
      "createdAt": "ISO 8601 date string"
    },
    "token": "JWT authentication token"
  }
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "fullName": "Full name must be at least 2 characters",
    "email": "Email is already registered",
    "password": "Password is too weak"
  }
}
```

---

### 2. User Login
**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
  "email": "string (required, valid email format)",
  "password": "string (required, min 6 characters)",
  "rememberMe": "boolean (optional, default: false)"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "string",
      "name": "string",
      "username": "string",
      "email": "string",
      "profilePhoto": "string (URL or base64)",
      "coverPhoto": "string (URL or base64)"
    },
    "token": "JWT authentication token",
    "expiresIn": "number (seconds, if rememberMe is true, use longer expiry)"
  }
}
```

**Response (Error - 401):**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

---

### 3. Forgot Password
**Endpoint:** `POST /api/auth/forgot-password`

**Request Body:**
```json
{
  "email": "string (required, valid email format)"
}
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

---

## User Profile Endpoints

### 4. Get User Profile
**Endpoint:** `GET /api/users/:userId` or `GET /api/users/me` (for current user)

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "name": "string",
    "username": "string (format: @username)",
    "bio": "string (max 160 characters, optional)",
    "location": "string (optional)",
    "website": "string (optional, format: example.com without https://)",
    "email": "string",
    "phone": "string (optional)",
    "joinDate": "string (format: 'Month YYYY', e.g., 'January 2020')",
    "coverPhoto": "string (URL)",
    "profilePhoto": "string (URL)",
    "friends": "number (count of friends)",
    "posts": "number (count of posts)",
    "projects": "number (count of projects)",
    "createdAt": "ISO 8601 date string"
  }
}
```

---

### 5. Update User Profile
**Endpoint:** `PUT /api/users/:userId` or `PUT /api/users/me`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data (for file uploads)
```

**Request Body (Form Data):**
```
name: string (required)
username: string (required, must start with @)
bio: string (optional, max 160 characters)
location: string (optional)
website: string (optional, format: example.com)
joinDate: string (optional, format: 'Month YYYY')
profilePhoto: File (optional, image file)
coverPhoto: File (optional, image file)
```

**Validation Rules:**
- `name`: Required, non-empty string
- `username`: Required, must start with '@'
- `website`: If provided, must match pattern: `^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- `bio`: Maximum 160 characters

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": "string",
    "name": "string",
    "username": "string",
    "bio": "string",
    "location": "string",
    "website": "string",
    "joinDate": "string",
    "profilePhoto": "string (URL)",
    "coverPhoto": "string (URL)",
    "updatedAt": "ISO 8601 date string"
  }
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "name": "Name is required",
    "username": "Username must start with @",
    "website": "Please enter a valid website (e.g., example.com)"
  }
}
```

---

### 6. Get User Friends/Connections
**Endpoint:** `GET /api/users/:userId/friends`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page`: number (optional, default: 1)
- `limit`: number (optional, default: 20)

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "friends": [
      {
        "id": "string",
        "name": "string",
        "avatar": "string (URL)",
        "status": "string (online | offline)",
        "mutualFriends": "number"
      }
    ],
    "pagination": {
      "page": "number",
      "limit": "number",
      "total": "number",
      "totalPages": "number"
    }
  }
}
```

---

## Posts Endpoints

### 7. Create Post
**Endpoint:** `POST /api/posts`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
description: string (required)
images: File[] (optional, multiple image files - only if no video)
video: File (optional, single video file - only if no images)
mediaType: string (optional, 'image' | 'video' | null)
```

**Validation Rules:**
- `description`: Required, non-empty string
- Media validation: Either upload multiple images OR one video, never both
- If `images` are provided, `video` must be null/empty
- If `video` is provided, `images` must be empty array
- Media is optional, but if provided, must follow the above rules

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Post created successfully",
  "data": {
    "id": "string",
    "author": "string (user name)",
    "authorId": "string",
    "content": "string",
    "images": ["string (URL)", ...],
    "video": "string (URL) or null",
    "mediaType": "string ('image' | 'video' | null)",
    "likes": "number (default: 0)",
    "comments": "number (default: 0)",
    "shares": "number (default: 0)",
    "createdAt": "ISO 8601 date string",
    "time": "string (relative time, e.g., '2 hours ago')"
  }
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "description": "Description is required",
    "media": "You can upload either one video OR multiple images, not both"
  }
}
```

---

### 8. Get Posts Feed
**Endpoint:** `GET /api/posts`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page`: number (optional, default: 1)
- `limit`: number (optional, default: 10)
- `userId`: string (optional, filter by specific user)

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "posts": [
      {
        "id": "string",
        "author": "string",
        "authorId": "string",
        "time": "string (relative time, e.g., '2 hours ago')",
        "content": "string",
        "images": ["string (URL)", ...],
        "video": "string (URL) or null",
        "likes": "number",
        "comments": "number",
        "shares": "number",
        "isLiked": "boolean (whether current user liked this post)",
        "createdAt": "ISO 8601 date string"
      }
    ],
    "pagination": {
      "page": "number",
      "limit": "number",
      "total": "number",
      "totalPages": "number"
    }
  }
}
```

---

### 9. Get Single Post
**Endpoint:** `GET /api/posts/:postId`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "author": "string",
    "authorId": "string",
    "time": "string",
    "content": "string",
    "images": ["string (URL)", ...],
    "video": "string (URL) or null",
    "likes": "number",
    "comments": "number",
    "shares": "number",
    "isLiked": "boolean",
    "createdAt": "ISO 8601 date string"
  }
}
```

---

### 10. Delete Post
**Endpoint:** `DELETE /api/posts/:postId`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Post deleted successfully"
}
```

---

## Social Interactions

### 11. Like/Unlike Post
**Endpoint:** `POST /api/posts/:postId/like` or `DELETE /api/posts/:postId/like`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Post liked" or "Post unliked",
  "data": {
    "postId": "string",
    "likes": "number (updated count)",
    "isLiked": "boolean"
  }
}
```

---

### 12. Share Post
**Endpoint:** `POST /api/posts/:postId/share`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Post shared",
  "data": {
    "postId": "string",
    "shares": "number (updated count)"
  }
}
```

---

### 13. Add Comment to Post
**Endpoint:** `POST /api/posts/:postId/comments`

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "content": "string (required, non-empty)"
}
```

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Comment added",
  "data": {
    "id": "string",
    "postId": "string",
    "authorId": "string",
    "author": "string",
    "content": "string",
    "createdAt": "ISO 8601 date string",
    "comments": "number (updated total comments count for post)"
  }
}
```

---

### 14. Get Post Comments
**Endpoint:** `GET /api/posts/:postId/comments`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `page`: number (optional, default: 1)
- `limit`: number (optional, default: 20)

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "comments": [
      {
        "id": "string",
        "authorId": "string",
        "author": "string",
        "authorAvatar": "string (URL)",
        "content": "string",
        "createdAt": "ISO 8601 date string",
        "time": "string (relative time)"
      }
    ],
    "pagination": {
      "page": "number",
      "limit": "number",
      "total": "number",
      "totalPages": "number"
    }
  }
}
```

---

## Projects Endpoints

### 15. Create Project
**Endpoint:** `POST /api/projects`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body (Form Data):**
```
title: string (required)
description: string (required)
techStack: string[] (required, at least one technology)
githubUrl: string (required, valid URL)
liveUrl: string (optional, valid URL)
category: string (optional, one of: 'web', 'mobile', 'desktop', 'api', 'ml', 'other')
dateCreated: string (optional, ISO 8601 date or YYYY-MM-DD format)
featured: boolean (optional, default: false)
images: File[] (optional, multiple image files)
```

**Validation Rules:**
- `title`: Required, non-empty string
- `description`: Required, non-empty string
- `techStack`: Required, array with at least one element
- `githubUrl`: Required, must be a valid URL
- `liveUrl`: Optional, but if provided, must be a valid URL
- `category`: Optional, must be one of the specified values

**Response (Success - 201):**
```json
{
  "success": true,
  "message": "Project created successfully",
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "techStack": ["string", ...],
    "githubUrl": "string",
    "liveUrl": "string or null",
    "category": "string",
    "dateCreated": "ISO 8601 date string",
    "featured": "boolean",
    "images": ["string (URL)", ...],
    "createdAt": "ISO 8601 date string"
  }
}
```

**Response (Error - 400):**
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "title": "Project title is required",
    "description": "Description is required",
    "techStack": "At least one technology is required",
    "githubUrl": "GitHub URL is required" or "Please enter a valid URL",
    "liveUrl": "Please enter a valid URL"
  }
}
```

---

### 16. Update Project
**Endpoint:** `PUT /api/projects/:projectId`

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:** Same as Create Project (all fields optional except validation rules apply)

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Project updated successfully",
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "techStack": ["string", ...],
    "githubUrl": "string",
    "liveUrl": "string or null",
    "category": "string",
    "dateCreated": "ISO 8601 date string",
    "featured": "boolean",
    "images": ["string (URL)", ...],
    "updatedAt": "ISO 8601 date string"
  }
}
```

---

### 17. Get User Projects
**Endpoint:** `GET /api/projects` or `GET /api/users/:userId/projects`

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `userId`: string (optional, filter by user)
- `featured`: boolean (optional, filter featured projects)
- `category`: string (optional, filter by category)
- `page`: number (optional, default: 1)
- `limit`: number (optional, default: 20)

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "projects": [
      {
        "id": "string",
        "userId": "string",
        "title": "string",
        "description": "string",
        "techStack": ["string", ...],
        "githubUrl": "string",
        "liveUrl": "string or null",
        "category": "string",
        "dateCreated": "ISO 8601 date string",
        "featured": "boolean",
        "images": ["string (URL)", ...],
        "createdAt": "ISO 8601 date string"
      }
    ],
    "pagination": {
      "page": "number",
      "limit": "number",
      "total": "number",
      "totalPages": "number"
    }
  }
}
```

---

### 18. Get Single Project
**Endpoint:** `GET /api/projects/:projectId`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "data": {
    "id": "string",
    "userId": "string",
    "title": "string",
    "description": "string",
    "techStack": ["string", ...],
    "githubUrl": "string",
    "liveUrl": "string or null",
    "category": "string",
    "dateCreated": "ISO 8601 date string",
    "featured": "boolean",
    "images": ["string (URL)", ...],
    "createdAt": "ISO 8601 date string"
  }
}
```

---

### 19. Delete Project
**Endpoint:** `DELETE /api/projects/:projectId`

**Headers:**
```
Authorization: Bearer <token>
```

**Response (Success - 200):**
```json
{
  "success": true,
  "message": "Project deleted successfully"
}
```

---

## General Notes

### Authentication
- All protected endpoints require a JWT token in the Authorization header: `Authorization: Bearer <token>`
- Token should be included in all requests except login and signup
- Token expiration should be handled (typically 24 hours, or longer if `rememberMe` is true)

### File Uploads
- Profile photos and cover photos: Accept image files (jpg, png, gif, webp)
- Post images: Accept multiple image files
- Post videos: Accept single video file (mp4, webm, etc.)
- Project images: Accept multiple image files
- Recommended max file sizes:
  - Profile/Cover photos: 5MB
  - Post images: 10MB per image
  - Post videos: 50MB
  - Project images: 10MB per image

### Error Responses
All error responses follow this format:
```json
{
  "success": false,
  "message": "Error message",
  "errors": {
    "fieldName": "Field-specific error message"
  }
}
```

Common HTTP Status Codes:
- `200`: Success
- `201`: Created
- `400`: Bad Request (validation errors)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (user doesn't have permission)
- `404`: Not Found
- `500`: Internal Server Error

### Date Formats
- Use ISO 8601 format for all date fields in API responses: `YYYY-MM-DDTHH:mm:ss.sssZ`
- For display purposes, frontend will format dates as relative time (e.g., "2 hours ago") or formatted dates (e.g., "January 2020")

### Pagination
All list endpoints should support pagination with these query parameters:
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 10-20, depending on endpoint)

Response should include pagination metadata:
```json
{
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### CORS
- Backend should allow CORS from frontend origin
- Include appropriate headers for preflight requests

### Rate Limiting
- Consider implementing rate limiting for authentication endpoints
- Recommended: 5 requests per minute for login/signup

---

## Summary of Required Endpoints

1. `POST /api/auth/signup` - User registration
2. `POST /api/auth/login` - User login
3. `POST /api/auth/forgot-password` - Password reset
4. `GET /api/users/:userId` - Get user profile
5. `PUT /api/users/:userId` - Update user profile
6. `GET /api/users/:userId/friends` - Get user friends
7. `POST /api/posts` - Create post
8. `GET /api/posts` - Get posts feed
9. `GET /api/posts/:postId` - Get single post
10. `DELETE /api/posts/:postId` - Delete post
11. `POST /api/posts/:postId/like` - Like post
12. `DELETE /api/posts/:postId/like` - Unlike post
13. `POST /api/posts/:postId/share` - Share post
14. `POST /api/posts/:postId/comments` - Add comment
15. `GET /api/posts/:postId/comments` - Get comments
16. `POST /api/projects` - Create project
17. `PUT /api/projects/:projectId` - Update project
18. `GET /api/projects` - Get projects
19. `GET /api/projects/:projectId` - Get single project
20. `DELETE /api/projects/:projectId` - Delete project

---