import { expect, test } from "@playwright/test";

test.describe("Login functionality", () => {
  test("should show login page when not authenticated", async ({ page }) => {
    // Clear any existing auth
    await page.goto("/");
    
    // Should be on login page
    await expect(page.getByRole("heading", { name: /sign in/i })).toBeVisible();
    await expect(page.getByLabel(/username/i)).toBeVisible();
    await expect(page.getByLabel(/password/i)).toBeVisible();
  });

  test("should show error with invalid credentials", async ({ page }) => {
    await page.goto("/");
    
    await page.getByLabel(/username/i).fill("wrong");
    await page.getByLabel(/password/i).fill("wrong");
    await page.getByRole("button", { name: /sign in/i }).click();
    
    await expect(page.getByText(/invalid credentials/i)).toBeVisible();
  });

  test("should redirect to kanban board with valid credentials", async ({ page }) => {
    await page.goto("/");
    
    await page.getByLabel(/username/i).fill("user");
    await page.getByLabel(/password/i).fill("password");
    await page.getByRole("button", { name: /sign in/i }).click();
    
    // Wait for kanban board to load
    await page.waitForSelector('[data-testid^="column-"]', { timeout: 10000 });
    
    // Should redirect to home page with kanban board
    await expect(page.getByRole("heading", { name: /kanban studio/i })).toBeVisible();
    // Check for 5 columns
    await expect(page.locator('[data-testid^="column-"]')).toHaveCount(5);
  });

  test("should logout and redirect to login", async ({ page }) => {
    // First login
    await page.goto("/");
    await page.getByLabel(/username/i).fill("user");
    await page.getByLabel(/password/i).fill("password");
    await page.getByRole("button", { name: /sign in/i }).click();
    
    // Wait for kanban board
    await expect(page.getByRole("heading", { name: /kanban studio/i }).first()).toBeVisible();
    
    // Click logout button (use first() to handle multiple matches)
    await page.getByRole("button", { name: /logout/i }).first().click();
    
    // Wait for redirect to login page
    await page.waitForURL("**/login", { timeout: 10000 });
    
    // Should be on login page
    await expect(page.getByRole("heading", { name: /sign in/i })).toBeVisible();
  });
});
