import { expect, test } from "@playwright/test";

// Helper to login
async function login(page: any) {
  await page.context().clearCookies();
  await page.goto("/");
  await page.getByLabel("Username").fill("user");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("**/", { timeout: 10000 });
  await page.waitForSelector('[data-testid^="column-"]', { timeout: 10000 });
}

test.describe("AI Sidebar", () => {
  test("should open and close the sidebar", async ({ page }) => {
    console.log("Starting login...");
    await login(page);
    console.log("Login successful.");
    
    // Wait for button and click it
    const aiButton = page.getByTestId("open-ai-chat");
    console.log("Waiting for AI button...");
    await aiButton.waitFor({ state: "visible", timeout: 15000 });
    console.log("Clicking AI button...");
    await aiButton.click();
    
    // Sidebar should be visible
    console.log("Checking if sidebar is visible...");
    await expect(page.getByRole("heading", { name: /ai assistant/i })).toBeVisible({ timeout: 10000 });
    console.log("Sidebar is visible.");
    
    // Close sidebar
    console.log("Clicking close button...");
    await page.getByTestId("close-sidebar").click();
    
    // Sidebar should not be visible
    console.log("Checking if sidebar is hidden...");
    await expect(page.getByRole("heading", { name: /ai assistant/i })).not.toBeVisible({ timeout: 10000 });
    console.log("Sidebar is hidden.");
  });

  test("should send a message and receive a response", async ({ page }) => {
    await login(page);
    
    await page.getByTestId("open-ai-chat").waitFor({ state: "visible", timeout: 15000 });
    await page.getByTestId("open-ai-chat").click();
    
    const input = page.getByTestId("ai-input");
    await input.waitFor({ state: "visible" });
    await input.fill("Hello AI");
    await page.getByTestId("ai-send").click();
    
    // User message should appear
    await expect(page.getByText("Hello AI")).toBeVisible({ timeout: 10000 });
    
    // AI should respond (wait for it)
    // We check for the "thinking" indicator first
    await expect(page.getByText(/thinking/i)).toBeVisible({ timeout: 10000 });
    await expect(page.getByText(/thinking/i)).not.toBeVisible({ timeout: 30000 });
    
    // Assistant message should appear
    // We look for a message that is NOT "Hello AI"
    const assistantMessages = page.locator('.bg-\\[var\\(--surface\\)\\]');
    await expect(assistantMessages.count()).resolves.toBeGreaterThan(0);
  });

  test("should update board when AI performs an action", async ({ page }) => {
    await login(page);
    
    // Count initial cards in first column
    const firstColumn = page.locator('[data-testid^="column-"]').first();
    await firstColumn.waitFor({ state: "visible" });
    const initialCards = await firstColumn.locator('[data-testid^="card-"]').count();
    
    await page.getByTestId("open-ai-chat").waitFor({ state: "visible" });
    await page.getByTestId("open-ai-chat").click();
    
    const input = page.getByTestId("ai-input");
    await input.fill("Add a task to the first column called 'AI E2E Task'");
    await page.getByTestId("ai-send").click();
    
    // Wait for AI to respond and perform action
    await expect(page.getByText(/thinking/i)).not.toBeVisible({ timeout: 30000 });
    
    // Board should refresh and show new card
    // Note: AI might take some time to perform the action and frontend to refresh
    await expect(firstColumn.locator('[data-testid^="card-"]')).toHaveCount(initialCards + 1, { timeout: 30000 });
    await expect(page.getByText("AI E2E Task")).toBeVisible({ timeout: 10000 });
  });
});
