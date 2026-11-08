
import api from "./client";

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface UserProfile {
  message: string;
  user_id: number;
}

// Login using our existing FastAPI endpoint
export async function loginUser(
  credentials: LoginCredentials
): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>(
    "/auth/login",
    credentials
  );

  return response.data;
}

// Register a new user
export async function registerUser(data: RegisterData) {
  const response = await api.post("/auth/register", data);

  return response.data;
}

// Retrieve the authenticated user's profile
export async function getMyProfile(
  accessToken: string
): Promise<UserProfile> {
  const response = await api.get<UserProfile>(
    "/auth/me",
    {
      headers: {
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  return response.data;
}
