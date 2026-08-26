/**
 * PawPawDoo DTC Storefront Interactive Logic & CRO Engine
 * Brand: PawPawDoo | Tagline: "Pawmily first."
 */

document.addEventListener('DOMContentLoaded', () => {
  initVariantSelectors();
  initBundleSelector();
  initCountdownTimer();
  initGallery();
  initFaqAccordion();
  initStickyCtaBar();
  initSocialProofPopups();
});

// 0. Variant Selectors (Size & Color - Rule #13)
let currentSelectedSize = 'M';
let currentSelectedColor = 'Cloud Cream';

function initVariantSelectors() {
  const sizeBtns = document.querySelectorAll('.size-option-btn');
  const sizeLabel = document.getElementById('selectedSizeLabel');
  
  sizeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      sizeBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      currentSelectedSize = btn.dataset.size;
      if (sizeLabel && btn.dataset.label) {
        sizeLabel.textContent = btn.dataset.label;
      }
    });
  });

  const colorBtns = document.querySelectorAll('.color-swatch-btn');
  const colorLabel = document.getElementById('selectedColorLabel');
  
  colorBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      colorBtns.forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      currentSelectedColor = btn.dataset.color;
      if (colorLabel) {
        colorLabel.textContent = currentSelectedColor;
      }
    });
  });
}

// 1. Bundle Selector & Checkout Engine
const BUNDLE_DATA = {
  1: {
    quantity: 1,
    title: '1x Orthopedic Cloud Pet Bed',
    price: 78.95,
    compareAt: 102.64,
    savings: '$23.69 (Save 23%)',
    badge: 'Standard Pack',
    bonus: 'Standard Packaging',
    sku: 'DS-PPD-BED-001',
    variantId: '15345170022445'
  },
  2: {
    quantity: 2,
    title: '2x Multi-Room / Multi-Pet Pack (Living Room + Bedroom)',
    price: 134.22,
    compareAt: 205.28,
    savings: '$71.06 (Save 15% Additional)',
    badge: 'BEST VALUE — 68% OF PET PARENTS CHOOSE THIS',
    bonus: 'Free Odor-Eliminating Paw Care Guide ($19.99 Value)',
    sku: 'DS-PPD-BED-002',
    variantId: '15345170022445'
  },
  3: {
    quantity: 3,
    title: '3x Ultimate Fur-Family Pack (Multi-Pet Household)',
    price: 185.53,
    compareAt: 307.92,
    savings: '$122.39 (Save 22% Additional)',
    badge: 'MAXIMUM SAVINGS',
    bonus: 'Free Spare Waterproof Cover + Grooming Glove ($39.99 Value)',
    sku: 'DS-PPD-BED-003',
    variantId: '15345170022445'
  }
};

let currentSelectedTier = 2; // Default to Tier 2 (Most Popular)

function initBundleSelector() {
  const cards = document.querySelectorAll('.bundle-card');
  const mainCtaText = document.getElementById('mainCtaText');
  const stickyPrice = document.getElementById('stickyPrice');
  const stickyBadge = document.getElementById('stickyBadge');

  cards.forEach(card => {
    card.addEventListener('click', () => {
      cards.forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
      
      const tier = parseInt(card.dataset.tier, 10);
      currentSelectedTier = tier;
      const data = BUNDLE_DATA[tier];

      if (mainCtaText) {
        mainCtaText.textContent = `Claim Your Pack — $${data.price.toFixed(2)} (Save ${tier === 1 ? '23%' : tier === 2 ? '35%' : '40%'})`;
      }
      if (stickyPrice) {
        stickyPrice.textContent = `$${data.price.toFixed(2)}`;
      }
      if (stickyBadge) {
        stickyBadge.textContent = tier === 2 ? 'Save 15%' : tier === 3 ? 'Save 22%' : 'Free Ship';
      }
    });
  });

  // Main CTA Click Handler
  const checkoutButtons = document.querySelectorAll('.trigger-checkout');
  checkoutButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      handleCheckout(currentSelectedTier);
    });
  });
}

function handleCheckout(tier) {
  const data = BUNDLE_DATA[tier];
  console.log(`[PawPawDoo Checkout] Initiating checkout for Tier ${tier}:`, data);
  
  // Construct direct Shopify checkout URL
  const shopifyDomain = 'pawpawdoo.store';
  const checkoutUrl = `https://${shopifyDomain}/cart/${data.variantId}:${data.quantity}?ref=pawpawdoo-direct`;
  
  // Open checkout or notify
  window.open(checkoutUrl, '_blank');
}

// 2. Real-Time Urgency Countdown Timer
function initCountdownTimer() {
  const timerElement = document.getElementById('flashSaleTimer');
  if (!timerElement) return;

  let totalSeconds = 4 * 3600 + 38 * 60 + 15; // 4 hours 38 mins

  setInterval(() => {
    if (totalSeconds <= 0) {
      totalSeconds = 24 * 3600; // Reset
    }
    totalSeconds--;

    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    timerElement.textContent = `${pad(hours)}:${pad(minutes)}:${pad(seconds)}`;
  }, 1000);
}

function pad(num) {
  return num < 10 ? '0' + num : num;
}

// 3. Multi-View Gallery Switcher
function initGallery() {
  const thumbs = document.querySelectorAll('.thumb-item');
  const mainImage = document.getElementById('mainHeroImage');

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');

      const newSrc = thumb.dataset.fullSrc;
      if (mainImage && newSrc) {
        mainImage.src = newSrc;
      }
    });
  });
}

// 4. FAQ & Sizing Accordion
function initFaqAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    question.addEventListener('click', () => {
      const isActive = item.classList.contains('active');
      faqItems.forEach(i => i.classList.remove('active'));
      if (!isActive) {
        item.classList.add('active');
      }
    });
  });
}

// 5. Mobile Sticky CTA Bar Trigger (Rule #4)
function initStickyCtaBar() {
  const stickyBar = document.getElementById('mobileStickyCta');
  if (!stickyBar) return;

  window.addEventListener('scroll', () => {
    const scrollPos = window.scrollY || window.pageYOffset;
    if (scrollPos > 320) {
      stickyBar.classList.add('visible');
    } else {
      stickyBar.classList.remove('visible');
    }
  });
}

// 6. Live Social Proof Ticker
function initSocialProofPopups() {
  const cities = ['Austin, TX', 'Seattle, WA', 'Denver, CO', 'Chicago, IL', 'San Diego, CA', 'Miami, FL', 'Nashville, TN'];
  const names = ['Jessica M.', 'David K.', 'Emily R.', 'Michael B.', 'Sarah T.', 'Amanda L.'];
  const packs = ['2-Pack Multi-Room Bundle', '1x Cloud Bed', '3-Pack Fur-Family Bundle'];

  const popup = document.createElement('div');
  popup.className = 'live-sales-popup';
  popup.style.cssText = `
    position: fixed;
    bottom: 90px;
    left: 20px;
    background: #FFFFFF;
    border: 1px solid #EADBCE;
    box-shadow: 0 8px 24px rgba(55,40,29,0.12);
    border-radius: 12px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    z-index: 999;
    transform: translateY(150px);
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    max-width: 320px;
    font-size: 13px;
  `;
  document.body.appendChild(popup);

  function showNotification() {
    const randomCity = cities[Math.floor(Math.random() * cities.length)];
    const randomName = names[Math.floor(Math.random() * names.length)];
    const randomPack = packs[Math.floor(Math.random() * packs.length)];
    const randomMins = Math.floor(Math.random() * 8) + 1;

    popup.innerHTML = `
      <div style="width: 38px; height: 38px; background: #F7EAE3; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 18px;">🐾</div>
      <div>
        <div style="font-weight: 700; color: #37281D;">${randomName} from ${randomCity}</div>
        <div style="color: #5E4A3E; font-size: 12px;">Purchased <strong>${randomPack}</strong> (${randomMins}m ago)</div>
      </div>
    `;

    popup.style.transform = 'translateY(0)';
    setTimeout(() => {
      popup.style.transform = 'translateY(150px)';
    }, 5000);
  }

  // First trigger after 6 seconds, then every 24 seconds
  setTimeout(() => {
    showNotification();
    setInterval(showNotification, 24000);
  }, 6000);
}

