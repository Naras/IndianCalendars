import { test, expect } from '@playwright/test';

test.describe('AstroCalendar Web Application E2E Tests', () => {

  test('should load page and check main title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/AstroCalendar/);
    
    // Verify header/logo rendering
    const logo = page.locator('.nav-logo');
    await expect(logo).toContainText('AstroCalendar');
  });

  test('should switch views between Calendar Gears and Panchanga Calculator', async ({ page }) => {
    await page.goto('/');
    
    // Default view should be Calendar Gears (wheels-view)
    const wheelsView = page.locator('#wheels-view');
    const panchangaView = page.locator('#panchanga-view');
    await expect(wheelsView).toHaveClass(/active/);
    await expect(panchangaView).not.toHaveClass(/active/);

    // Switch to Panchanga Calculator
    const panchangaTab = page.locator('button.nav-tab[data-target="panchanga-view"]');
    await panchangaTab.click();
    await expect(panchangaView).toHaveClass(/active/);
    await expect(wheelsView).not.toHaveClass(/active/);

    // Switch back to Calendar Gears
    const wheelsTab = page.locator('button.nav-tab[data-target="wheels-view"]');
    await wheelsTab.click();
    await expect(wheelsView).toHaveClass(/active/);
    await expect(panchangaView).not.toHaveClass(/active/);
  });

  test('should fine-tune date inputs using increment/decrement controls', async ({ page }) => {
    await page.goto('/');
    
    // Go to Panchanga tab
    await page.locator('button.nav-tab[data-target="panchanga-view"]').click();

    // Set custom date
    const dateInput = page.locator('#panchanga-date');
    await dateInput.fill('1992-04-13');

    // Click increment year
    await page.locator('#inc-year').click();
    
    // The date input should update to 1993-04-13
    await expect(dateInput).toHaveValue('1993-04-13');
    await expect(page.locator('#val-year')).toHaveText('1993');

    // Click decrement day
    await page.locator('#dec-day').click();
    
    // The date input should update to 1993-04-12
    await expect(dateInput).toHaveValue('1993-04-12');
    await expect(page.locator('#val-day')).toHaveText('12');
  });

  test('should intercept network API requests and render computed Panchanga results', async ({ page }) => {
    await page.goto('/');
    
    // Intercept /api/panchanga network call and return mock data
    await page.route('**/api/panchanga*', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          name: "Test User",
          place: "Bangalore, India",
          date: "1992-04-13 16:28",
          ascendant: "Scorpio",
          "moon sign": "Leo",
          nakshatra: "Magha",
          tithi: "Shukla Dwadashi",
          yoga: "Ganda",
          karana: "Bava",
          vaara: "Monday"
        })
      });
    });

    // Go to Panchanga tab
    await page.locator('button.nav-tab[data-target="panchanga-view"]').click();

    // Fill the inputs
    await page.locator('#panchanga-name').fill('Test User');
    await page.locator('#panchanga-place').fill('Bangalore, India');
    await page.locator('#panchanga-date').fill('1992-04-13');
    await page.locator('#panchanga-time').fill('16:28');

    // Click submit
    await page.locator('#panchanga-submit').click();

    // Wait for the results container to be visible and assert correctly filled mocks
    const resultsContainer = page.locator('#panchanga-results-container');
    await expect(resultsContainer).toBeVisible();

    await expect(page.locator('#res-name')).toHaveText('Test User');
    await expect(page.locator('#res-place')).toHaveText('Bangalore, India');
    await expect(page.locator('#res-ascendant')).toHaveText('Scorpio');
    await expect(page.locator('#res-moonsign')).toHaveText('Leo');
    await expect(page.locator('#res-nakshatra')).toHaveText('Magha');
    await expect(page.locator('#res-tithi')).toHaveText('Shukla Dwadashi');
    await expect(page.locator('#res-yoga')).toHaveText('Ganda');
    await expect(page.locator('#res-karana')).toHaveText('Bava');
    await expect(page.locator('#res-vaara')).toHaveText('Monday');
  });
});
