"use client";

import { render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import LoginPage from "@/app/login/page";

// Mock next/navigation
const pushMock = vi.fn();
vi.mock("next/navigation", () => ({
  useRouter: vi.fn(() => ({
    push: pushMock,
  })),
}));

describe("LoginPage", () => {
  beforeEach(() => {
    // Clear mocks before each test
    vi.clearAllMocks();
    localStorage.clear();
  });

  it("renders login form", () => {
    render(<LoginPage />);
    expect(screen.getByRole("heading", { name: /sign in/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign in/i })).toBeInTheDocument();
  });

  it("shows error with invalid credentials", async () => {
    render(<LoginPage />);
    const user = userEvent.setup();
    
    await user.type(screen.getByLabelText(/username/i), "wrong");
    await user.type(screen.getByLabelText(/password/i), "wrong");
    await user.click(screen.getByRole("button", { name: /sign in/i }));
    
    expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
  });

  it("calls router.push with valid credentials", async () => {
    render(<LoginPage />);
    const user = userEvent.setup();
    
    await user.type(screen.getByLabelText(/username/i), "user");
    await user.type(screen.getByLabelText(/password/i), "password");
    await user.click(screen.getByRole("button", { name: /sign in/i }));
    
    // Check localStorage was set
    expect(localStorage.getItem("auth")).toBe("true");
    expect(pushMock).toHaveBeenCalledWith("/");
  });
});
