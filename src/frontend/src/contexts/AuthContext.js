import { createContext, useState } from "react";

export const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setAuthStatus] = useState(false);

  const logout = () => {
    setAuthStatus(false);
  };

  return <AuthContext.Provider value={{ isAuthenticated, setAuthStatus, logout }}>{children}</AuthContext.Provider>;
};
