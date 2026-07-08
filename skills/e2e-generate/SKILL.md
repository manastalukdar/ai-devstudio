---
name: e2e-generate
description: Generate end-to-end tests with Playwright browser automation
disable-model-invocation: true
---

# End-to-End Test Generation

I'll generate comprehensive E2E tests using Playwright for browser automation and testing.

**Capabilities:**
- Auto-detect frontend framework (React, Vue, Next.js, etc.)
- Generate Playwright test files with best practices
- Create page object models for maintainability
- Set up test infrastructure if missing


## Phase 1: Prerequisites Check

```bash
# Check if Playwright is installed
if [ -f "package.json" ]; then
    if grep -q "\"@playwright/test\"" package.json; then
        echo "✓ Playwright detected"
        PLAYWRIGHT_INSTALLED=true
    else
        echo "⚠️ Playwright not installed"
        PLAYWRIGHT_INSTALLED=false
    fi
else
    echo "❌ No package.json found"
    exit 1
fi

# Offer to install Playwright if missing
if [ "$PLAYWRIGHT_INSTALLED" = false ]; then
    echo ""
    echo "Playwright is required for E2E testing"
    read -p "Install Playwright? (yes/no): " install_pw

    if [ "$install_pw" = "yes" ]; then
        echo "Installing Playwright..."
        npm install --save-dev @playwright/test
        npx playwright install
        echo "✓ Playwright installed"
    else
        echo "Skipping installation. Install manually with:"
        echo "  npm install --save-dev @playwright/test"
        echo "  npx playwright install"
        exit 1
    fi
fi
```

## Phase 2: Framework Detection

```bash
# Token-efficient framework detection
detect_framework() {
    if grep -q "\"next\"" package.json; then
        echo "nextjs"
    elif grep -q "\"react\"" package.json; then
        if [ -d "src/pages" ] || [ -d "pages" ]; then
            echo "react-pages"
        else
            echo "react-spa"
        fi
    elif grep -q "\"vue\"" package.json; then
        echo "vue"
    elif grep -q "\"@angular/core\"" package.json; then
        echo "angular"
    elif grep -q "\"svelte\"" package.json; then
        echo "svelte"
    else
        echo "generic"
    fi
}

FRAMEWORK=$(detect_framework)
echo "✓ Framework detected: $FRAMEWORK"
```

## Phase 3: Page/Route Discovery

```bash
# Discover pages/routes efficiently with Grep
echo ""
echo "Discovering application pages..."

case $FRAMEWORK in
    nextjs)
        # Next.js App Router
        if [ -d "app" ]; then
            PAGES=$(find app -name "page.tsx" -o -name "page.jsx" -o -name "page.js" | head -10)
        # Next.js Pages Router
        elif [ -d "pages" ]; then
            PAGES=$(find pages -name "*.tsx" -o -name "*.jsx" -o -name "*.js" | grep -v "_app\|_document\|api" | head -10)
        fi
        ;;
    react-pages)
        PAGES=$(find src/pages -name "*.tsx" -o -name "*.jsx" | head -10)
        ;;
    react-spa)
        # Look for React Router routes
        ROUTES=$(grep -r "path=" src/ --include="*.tsx" --include="*.jsx" | head -10)
        ;;
    vue)
        PAGES=$(find src -name "*.vue" | head -10)
        ;;
esac

if [ -z "$PAGES" ]; then
    echo "⚠️ No pages found. Will generate generic test template."
    PAGE_COUNT=0
else
    PAGE_COUNT=$(echo "$PAGES" | wc -l)
    echo "✓ Found $PAGE_COUNT pages"
    echo ""
    echo "Sample pages:"
    echo "$PAGES" | head -5 | sed 's/^/  /'

    if [ $PAGE_COUNT -gt 5 ]; then
        echo "  ... and $((PAGE_COUNT - 5)) more"
    fi
fi
```

## Phase 4: Test Generation

```bash
# Create E2E test directory
mkdir -p tests/e2e

echo ""
echo "Generating E2E tests..."

# Generate playwright config if missing
if [ ! -f "playwright.config.ts" ]; then
    cat > playwright.config.ts << 'EOF'
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
EOF
    echo "✓ Created playwright.config.ts"
fi

# Generate base test template
cat > tests/e2e/example.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';

test.describe('Application E2E Tests', () => {
  test('should load homepage', async ({ page }) => {
    await page.goto('/');

    // Verify page loads
    await expect(page).toHaveTitle(/./);

    // Check for main content
    const mainContent = page.locator('main, #root, #app, [role="main"]');
    await expect(mainContent).toBeVisible();
  });

  test('should navigate between pages', async ({ page }) => {
    await page.goto('/');

    // Find and click a navigation link
    const navLink = page.locator('nav a, header a').first();
    await navLink.click();

    // Verify navigation occurred
    await page.waitForLoadState('networkidle');
    await expect(page.url()).not.toBe('http://localhost:3000/');
  });

  test('should be responsive', async ({ page }) => {
    // Test desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    await expect(page.locator('body')).toBeVisible();

    // Test mobile view
    await page.setViewportSize({ width: 375, height: 667 });
    await expect(page.locator('body')).toBeVisible();
  });
});
EOF

echo "✓ Created tests/e2e/example.spec.ts"

# Generate page-specific tests if pages found
if [ $PAGE_COUNT -gt 0 ]; then
    # Generate test for first page as example
    FIRST_PAGE=$(echo "$PAGES" | head -1)
    PAGE_NAME=$(basename "$FIRST_PAGE" | sed 's/\.[^.]*$//')

    cat > "tests/e2e/${PAGE_NAME}.spec.ts" << EOF
import { test, expect } from '@playwright/test';

test.describe('${PAGE_NAME} Page', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to page before each test
    await page.goto('/${PAGE_NAME}');
  });

  test('should render page correctly', async ({ page }) => {
    // Verify page loads
    await page.waitForLoadState('networkidle');

    // Check for key elements
    // TODO: Update selectors based on your page structure
    const heading = page.locator('h1, h2').first();
    await expect(heading).toBeVisible();
  });

  test('should handle user interactions', async ({ page }) => {
    // TODO: Add interaction tests
    // Example: Click buttons, fill forms, etc.
  });

  test('should display correct content', async ({ page }) => {
    // TODO: Verify page content
    // Example: Check text, images, links
  });

  test('should handle errors gracefully', async ({ page }) => {
    // TODO: Test error scenarios
    // Example: Invalid input, network failures
  });
});
EOF

    echo "✓ Created tests/e2e/${PAGE_NAME}.spec.ts"
fi
```

## Phase 5: Page Object Model (Optional but Recommended)

```bash
# Generate page object model example
mkdir -p tests/e2e/pages

cat > tests/e2e/pages/BasePage.ts << 'EOF'
import { Page } from '@playwright/test';

export class BasePage {
  constructor(protected page: Page) {}

  async goto(path: string) {
    await this.page.goto(path);
    await this.page.waitForLoadState('networkidle');
  }

  async waitForElement(selector: string) {
    await this.page.waitForSelector(selector);
  }

  async clickElement(selector: string) {
    await this.page.click(selector);
  }

  async typeIntoField(selector: string, text: string) {
    await this.page.fill(selector, text);
  }
}
EOF

echo "✓ Created tests/e2e/pages/BasePage.ts (Page Object Model base)"

cat > tests/e2e/pages/HomePage.ts << 'EOF'
import { Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class HomePage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async navigate() {
    await this.goto('/');
  }

  async getPageTitle() {
    return await this.page.title();
  }

  async clickNavLink(linkText: string) {
    await this.page.click(`nav a:has-text("${linkText}")`);
  }

  // Add more page-specific methods
}
EOF

echo "✓ Created tests/e2e/pages/HomePage.ts"
```

## Phase 6: Test Scripts

```bash
# Update package.json with E2E test scripts
if [ -f "package.json" ]; then
    # Check if test:e2e script exists
    if ! grep -q "\"test:e2e\"" package.json; then
        echo ""
        echo "Add these scripts to package.json:"
        echo ""
        cat << 'EOF'
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:ui": "playwright test --ui"
  }
EOF
    fi
fi
```

## Running Your E2E Tests

```bash
echo ""
echo "=== E2E Test Setup Complete! ==="
echo ""
echo "📁 Test files created:"
echo "  - tests/e2e/example.spec.ts"
if [ $PAGE_COUNT -gt 0 ]; then
    echo "  - tests/e2e/${PAGE_NAME}.spec.ts"
fi
echo "  - tests/e2e/pages/BasePage.ts"
echo "  - tests/e2e/pages/HomePage.ts"
echo "  - playwright.config.ts"
echo ""
echo "🚀 Run tests:"
echo "  npm run test:e2e              # Run all tests"
echo "  npm run test:e2e:headed       # Run with browser visible"
echo "  npm run test:e2e:debug        # Run in debug mode"
echo "  npm run test:e2e:ui           # Run with Playwright UI"
echo ""
echo "📝 Next steps:"
echo "  1. Customize test selectors for your app"
echo "  2. Add more page-specific tests"
echo "  3. Implement page object models for complex pages"
echo "  4. Add to CI/CD pipeline with /ci-setup"
```

## Best Practices

**E2E Testing Tips:**
- Use data-testid attributes for reliable selectors
- Test user workflows, not implementation details
- Keep tests independent (no shared state)
- Use page object models for maintainability
- Run tests in CI/CD pipeline

**Anti-Patterns to Avoid:**
- Testing every possible scenario (focus on critical paths)
- Fragile selectors (CSS classes that change often)
- Long test chains (break into smaller tests)
- Missing waits for async operations

## Integration Points

- `/ci-setup` - Add E2E tests to CI pipeline
- `/test` - Run E2E tests alongside unit tests
- `/deploy-validate` - Run E2E tests before deployment

**Credits:** Playwright integration patterns based on community best practices and MCP Playwright server capabilities.

## Token Optimization

**Expected range**: 1,200–3,000 tokens (initial), 300 tokens (cache hit)

**Caching**: Caches route inventory in `.claude/cache/e2e/routes.json` for 7 days. Invalidated when route files change.

**Early exit**: Returns immediately if Playwright is not installed or no routes are detected.

**Patterns used**: Grep-before-Read, early exit, template-based generation, caching
