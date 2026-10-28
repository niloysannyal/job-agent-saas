import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext(null);

const API_BASE = '/api/v1';
const TOKEN_KEY = 'jobeazy_jwt_token';
const SUPERADMIN_BACKUP_KEY = 'jobeazy_superadmin_token';

export function parseJwtPayload(token) {
  if (!token || typeof token !== 'string') return null;
  try {
    const parts = token.split('.');
    if (parts.length < 2) return null;
    const base64Url = parts[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );
    const parsed = JSON.parse(jsonPayload);
    if (parsed.exp && parsed.exp * 1000 < Date.now()) {
      return null;
    }
    return {
      id: parsed.sub,
      email: parsed.email,
      role: parsed.role,
      plan_tier: parsed.plan_tier,
      status: 'active',
    };
  } catch {
    return null;
  }
}

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => {
    if (typeof window === 'undefined') return '';
    return localStorage.getItem(TOKEN_KEY) || '';
  });
  const [user, setUser] = useState(() => {
    if (typeof window === 'undefined') return null;
    const stored = localStorage.getItem(TOKEN_KEY);
    return parseJwtPayload(stored);
  });
  const [isLoading, setIsLoading] = useState(false);
  const [impersonatedTenant, setImpersonatedTenant] = useState(null);

  // Validate token on mount
  useEffect(() => {
    const initAuth = async () => {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      if (!storedToken) {
        setUser(null);
        return;
      }

      try {
        const res = await fetch(`${API_BASE}/auth/me`, {
          headers: { Authorization: `Bearer ${storedToken}` },
        });

        if (res.ok) {
          const userData = await res.json();
          setUser(userData);
          setToken(storedToken);
        } else {
          // Token expired or invalid on server
          localStorage.removeItem(TOKEN_KEY);
          setToken('');
          setUser(null);
        }
      } catch (err) {
        console.error('Failed to verify session token:', err);
      }
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Authentication failed. Please check your credentials.');
    }

    const data = await res.json();
    localStorage.setItem(TOKEN_KEY, data.access_token);
    setToken(data.access_token);
    setUser({
      id: data.account_id,
      email: data.email,
      role: data.role,
      plan_tier: data.plan_tier,
      status: 'active',
    });
    setImpersonatedTenant(null);
    return data;
  };

  const register = async (email, password) => {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || 'Registration failed.');
    }

    const data = await res.json();
    localStorage.setItem(TOKEN_KEY, data.access_token);
    setToken(data.access_token);
    setUser({
      id: data.account_id,
      email: data.email,
      role: data.role,
      plan_tier: data.plan_tier,
      status: 'active',
    });
    setImpersonatedTenant(null);
    return data;
  };

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(SUPERADMIN_BACKUP_KEY);
    setToken('');
    setUser(null);
    setImpersonatedTenant(null);
  };

  // Superadmin QA Dogfooding: Impersonate a tenant
  const impersonateTenant = (tenant) => {
    if (!user || user.role !== 'superadmin') return;
    localStorage.setItem(SUPERADMIN_BACKUP_KEY, token);
    setImpersonatedTenant(tenant);
  };

  const exitImpersonation = () => {
    const originalToken = localStorage.getItem(SUPERADMIN_BACKUP_KEY);
    if (originalToken) {
      localStorage.setItem(TOKEN_KEY, originalToken);
      localStorage.removeItem(SUPERADMIN_BACKUP_KEY);
      setToken(originalToken);
    }
    setImpersonatedTenant(null);
  };

  // Active account ID is the impersonated tenant or the authenticated user
  const effectiveAccountId = impersonatedTenant ? impersonatedTenant.id : user?.id;

  const authHeaders = {
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    ...(effectiveAccountId ? { 'X-Account-ID': effectiveAccountId } : {}),
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        user,
        isAuthenticated: !!user,
        isSuperadmin: user?.role === 'superadmin',
        isImpersonating: !!impersonatedTenant,
        isLoading,
        impersonatedTenant,
        effectiveAccountId,
        authHeaders,
        login,
        register,
        logout,
        impersonateTenant,
        exitImpersonation,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
