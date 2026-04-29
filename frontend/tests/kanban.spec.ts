import { expect, test } from "@playwright/test";

// Helper to login
async function login(page: any) {
  // Clear any existing auth
  await page.context().clearCookies();
  
  await page.goto("/");
  
  // Wait for page to load
  await page.waitForLoadState("networkidle");
    
  // Check if we need to login by looking for login button
  const loginButton = page.getByRole("button", { name: "Sign in" });
  const isLoginPage = await loginButton.isVisible().catch(() => false);
    
  if (isLoginPage) {
    await page.getByLabel("Username").fill("user");
    await page.getByLabel("Password").fill("password");
    await loginButton.click();
    // Wait for redirect to kanban board
    await page.waitForURL("**/", { timeout: 10000 });
    await page.waitForLoadState("networkidle");
  }
    
  // Wait for kanban board to be visible
  await page.waitForSelector('[data-testid^="column-"]', { timeout: 10000 });
}

test("loads the kanban board", async ({ page }) => {
  await login(page);
  await expect(page.getByRole("heading", { name: "Kanban Studio" })).toBeVisible();
  await expect(page.locator('[data-testid^="column-"]')).toHaveCount(5);
});

test("adds a card to a column", async ({ page }) => {
  await login(page);
  const firstColumn = page.locator('[data-testid^="column-"]').first();
  await firstColumn.getByRole("button", { name: /add a card/i }).click();
  await firstColumn.getByPlaceholder("Card title").fill("Playwright card");
  await firstColumn.getByPlaceholder("Details").fill("Added via e2e.");
  await firstColumn.getByRole("button", { name: /add card/i }).click();
  await expect(firstColumn.getByText("Playwright card")).toBeVisible();
});

test("moves a card between columns", async ({ page }) => {
  await login(page);
  const card = page.getByTestId("card-card-1");
  const targetColumn = page.getByTestId("column-col-review");
  const cardBox = await card.boundingBox();
  const columnBox = await targetColumn.boundingBox();
  if (!cardBox || !columnBox) {
    throw new Error("Unable to resolve drag coordinates.");
  }

  await page.mouse.move(
    cardBox.x + cardBox.width / 2,
    cardBox.y + cardBox.height / 2
  );
  await page.mouse.down();
  await page.mouse.move(
    columnBox.x + columnBox.width / 2,
    columnBox.y + 120,
    { steps: 12 }
  );
  await page.mouse.up();
  await expect(targetColumn.getByTestId("card-card-1")).toBeVisible();
});
