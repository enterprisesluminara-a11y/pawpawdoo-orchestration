/**
 * PawPawDoo Flagship DTC E-Commerce JavaScript Engine
 * Brand: PawPawDoo | Slogan: "Pawmily first."
 */

document.addEventListener('DOMContentLoaded', () => {
  initGallery();
  initVariantCustomizer();
  initBundleTiers();
  initCountdownTimer();
  initFaqAccordion();
  initStickyCtaBar();
  initLiveSalesToasts();
});

// 1. Interactive Gallery
function initGallery() {
  const thumbs = document.querySelectorAll('.thumb-card');
  const mainPhoto = document.getElementById('mainHeroPhoto');

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');

      const targetSrc = thumb.dataset.src;
      if (mainPhoto && targetSrc) {
        mainPhoto.style.opacity = '0.3';
        setTimeout(() => {
          mainPhoto.src = targetSrc;
          mainPhoto.style.opacity = '1';
        }, 150);
      }
    });
  });
}

// 2. Variant Customizer (Size & Color)
let currentSize = 'M';
let currentColor = 'Cream Velvet';

function initVariantCustomizer() {
  const sizeChips = document.querySelectorAll('.size-chip');
  const sizeDisplay = document.getElementById('sizeValueDisplay');

  sizeChips.forEach(chip => {
    chip.addEventListener('click', () => {
      sizeChips.forEach(c => c.classList.remove('selected'));
      chip.classList.add('selected');
      currentSize = chip.dataset.size;
      if (sizeDisplay && chip.dataset.label) {
        sizeDisplay.textContent = chip.dataset.label;
      }
    });
  });

  const colorCards = document.querySelectorAll('.color-swatch-card');
  const colorDisplay = document.getElementById('colorValueDisplay');
  const mainPhoto = document.getElementById('mainHeroPhoto');

  const colorToImageMap = {
    'Cream Velvet': 'https://images.unsplash.com/photo-1541599540903-216a46ca1dc0?auto=format&fit=crop&w=1000&q=80',
    'Terracotta Cloud': 'https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?auto=format&fit=crop&w=1000&q=80',
    'Slate Grey': 'https://images.unsplash.com/photo-1548199973-03cce0bbc87b?auto=format&fit=crop&w=1000&q=80'
  };

  colorCards.forEach(card => {
    card.addEventListener('click', () => {
      colorCards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      currentColor = card.dataset.color;
      if (colorDisplay) {
        colorDisplay.textContent = currentColor;
      }
      if (mainPhoto && colorToImageMap[currentColor]) {
        mainPhoto.style.opacity = '0.3';
        setTimeout(() => {
          mainPhoto.src = colorToImageMap[currentColor];
          mainPhoto.style.opacity = '1';
        }, 150);
      }
    });
  });
}

// 3. Bundle Tiers & Checkout Engine
const BUNDLES = {
  1: {
    tier: 1,
    quantity: 1,
    title: '1x Calming Cloud Pet Bed',
    price: 78.95,
    compareAt: 102.64,
    saveText: '23%',
    variantId: '15345953112109'
  },
  2: {
    tier: 2,
    quantity: 2,
    title: '2x Multi-Room / Multi-Pet Pack',
    price: 134.22,
    compareAt: 205.28,
    saveText: '35%',
    badge: 'Save 15%',
    variantId: '15345953112109'
  },
  3: {
    tier: 3,
    quantity: 3,
    title: '3x Ultimate Fur-Family Pack',
    price: 185.53,
    compareAt: 307.92,
    saveText: '40%',
    badge: 'Save 22%',
    variantId: '15345953112109'
  }
};

let currentTier = 2; // Default to Tier 2 (Most Popular)

function initBundleTiers() {
  const cards = document.querySelectorAll('.bundle-tier-card');
  const mainCtaText = document.getElementById('mainCtaButtonText');
  const stickyPriceText = document.getElementById('stickyPriceText');
  const stickyBadgeText = document.getElementById('stickyBadgeText');
  const headerCartCount = document.getElementById('headerCartCount');

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');

      currentTier = parseInt(card.dataset.tier, 10);
      const b = BUNDLES[currentTier];

      if (mainCtaText) {
        mainCtaText.textContent = `Claim Your Pack — $${b.price.toFixed(2)} (Save ${b.saveText})`;
      }
      if (stickyPriceText) {
        stickyPriceText.textContent = `$${b.price.toFixed(2)}`;
      }
      if (stickyBadgeText) {
        stickyBadgeText.textContent = b.badge || 'Free Ship';
      }
      if (headerCartCount) {
        headerCartCount.textContent = b.quantity;
      }
    });
  });

  const triggers = document.querySelectorAll('.trigger-checkout');
  triggers.forEach(btn => {
    btn.addEventListener('click', () => {
      triggerShopifyCheckout(currentTier);
    });
  });
}

function triggerShopifyCheckout(tier) {
  const b = BUNDLES[tier];
  console.log(`[PawPawDoo Checkout] Initiating Checkout for Tier ${tier}:`, b);

  const domain = 'pawpawdoo.store';
  const checkoutUrl = `https://${domain}/cart/${b.variantId}:${b.quantity}?attributes[Size]=${encodeURIComponent(currentSize)}&attributes[Color]=${encodeURIComponent(currentColor)}&ref=pawpawdoo-direct`;
  window.open(checkoutUrl, '_blank');
}

// 4. Urgency Countdown Timer
function initCountdownTimer() {
  const timer = document.getElementById('flashTimer');
  if (!timer) return;

  let totalSeconds = 4 * 3600 + 38 * 60 + 15;

  setInterval(() => {
    if (totalSeconds <= 0) totalSeconds = 24 * 3600;
    totalSeconds--;

    const h = Math.floor(totalSeconds / 3600);
    const m = Math.floor((totalSeconds % 3600) / 60);
    const s = totalSeconds % 60;

    timer.textContent = `${pad(h)}:${pad(m)}:${pad(s)}`;
  }, 1000);
}

function pad(n) {
  return n < 10 ? '0' + n : n;
}

// 5. FAQ Accordion
function initFaqAccordion() {
  const items = document.querySelectorAll('.faq-accordion-item');

  items.forEach(item => {
    const btn = item.querySelector('.faq-accordion-btn');
    btn.addEventListener('click', () => {
      const isAlreadyActive = item.classList.contains('active');
      items.forEach(i => i.classList.remove('active'));
      if (!isAlreadyActive) {
        item.classList.add('active');
      }
    });
  });
}

// 6. Mobile Sticky CTA Bar
function initStickyCtaBar() {
  const bar = document.getElementById('mobileStickyBar');
  if (!bar) return;

  window.addEventListener('scroll', () => {
    const scroll = window.scrollY || window.pageYOffset;
    if (scroll > 250) {
      bar.classList.add('visible');
    } else {
      bar.classList.remove('visible');
    }
  });
}

// 7. Live Sales Toast Notifications
function initLiveSalesToasts() {
  const cities = ['Austin, TX', 'Seattle, WA', 'Denver, CO', 'Chicago, IL', 'San Diego, CA', 'Miami, FL', 'Nashville, TN'];
  const parents = ['Sarah & Duke 🐕', 'Elena & Oliver 🐱', 'Chloe & Dave 🐾', 'Marcus & Luna 🐶', 'Jessica & Cleo 🐱'];
  const bundles = ['2-Pack Multi-Room (Cream Velvet)', '1x Calming Bed (Terracotta Cloud)', '3-Pack Fur-Family (Slate Grey)'];

  const toast = document.createElement('div');
  toast.className = 'live-sale-toast';
  toast.style.cssText = `
    position: fixed;
    bottom: 84px;
    left: 20px;
    background: #FFFFFF;
    border: 1px solid #E8DFD5;
    box-shadow: 0 10px 28px rgba(42,31,24,0.12);
    border-radius: 14px;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 998;
    transform: translateY(160px);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    max-width: 320px;
    font-size: 13px;
  `;
  document.body.appendChild(toast);

  function triggerToast() {
    const rCity = cities[Math.floor(Math.random() * cities.length)];
    const rParent = parents[Math.floor(Math.random() * parents.length)];
    const rBundle = bundles[Math.floor(Math.random() * bundles.length)];
    const rMins = Math.floor(Math.random() * 8) + 1;

    toast.innerHTML = `
      <div style="width: 38px; height: 38px; background: #FBF0EB; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px;">🐾</div>
      <div>
        <div style="font-weight: 700; color: #2A1F18;">${rParent} in ${rCity}</div>
        <div style="color: #5E524A; font-size: 12px;">Purchased <strong>${rBundle}</strong> (${rMins}m ago)</div>
      </div>
    `;

    toast.style.transform = 'translateY(0)';
    setTimeout(() => {
      toast.style.transform = 'translateY(160px)';
    }, 5000);
  }

  setTimeout(() => {
    triggerToast();
    setInterval(triggerToast, 22000);
  }, 4000);
}
