class WIcartDrawer extends HTMLElement {
  constructor() {
    super();
    this.addEventListener("click", this.closeCart.bind(this));
    this.addEventListener("click", this.incQuantity.bind(this));
    this.addEventListener("click", this.decQuantity.bind(this));
    this.addEventListener("click", this.revQuantity.bind(this));
    this.addEventListener("click", this.cartBgclick.bind(this));
    this.addEventListener("click", this.handleCartClicks.bind(this));
    this.addEventListener("input", this.handleCartInputs.bind(this));
    this.addEventListener("submit", this.handleCartSubmits.bind(this));
    this.isProcessing = false;
    this._updateQueue = Promise.resolve();
    this._recsAbort = null;
    this._lastUpdate = 0;
  }

  wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  escapeAttr(value) {
    if (window.CSS && CSS.escape) return CSS.escape(value);
    return String(value).replace(/["\\]/g, "\\$&");
  }

  escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  routesRoot() {
    return (window.Shopify && Shopify.routes && Shopify.routes.root) || "/";
  }

  formatMoney(cents) {
    const currency =
      (window.Shopify && Shopify.currency && Shopify.currency.active) || "GBP";
    const locale = currency === "GBP" ? "en-GB" : undefined;
    try {
      return (Number(cents) / 100).toLocaleString(locale || undefined, {
        style: "currency",
        currency,
      });
    } catch (err) {
      return "£" + (Number(cents) / 100).toFixed(2);
    }
  }

  clearLoadingStates() {
    this.querySelectorAll(".wi-cart-item-loader").forEach((el) =>
      el.classList.add("hidden")
    );
    this.querySelectorAll(".wi-cart-qty-loader").forEach((el) =>
      el.classList.add("hidden")
    );
    this.querySelectorAll(".WI_cartDrawer_item").forEach((el) =>
      el.classList.remove("wi-cart-item--loading")
    );
    this.setGlobalLoading(false);
  }

  setGlobalLoading(loading) {
    const loader = this.querySelector(".wi-cart-global-loader");
    if (loader) loader.classList.toggle("hidden", !loading);
    this.classList.toggle("wi-cart-drawer--loading", loading);
  }

  setItemLoading(itemEl, loading) {
    if (!itemEl) return;
    const overlay = itemEl.querySelector(".wi-cart-item-loader");
    const qtyLoader = itemEl.querySelector(".wi-cart-qty-loader");
    itemEl.classList.toggle("wi-cart-item--loading", loading);
    if (overlay) overlay.classList.toggle("hidden", !loading);
    if (qtyLoader) qtyLoader.classList.toggle("hidden", !loading);
  }

  getItemKeys(container) {
    if (!container) return [];
    return [...container.querySelectorAll(".WI_cartDrawer_item")]
      .map((el) => el.getAttribute("data-itemKey"))
      .filter(Boolean);
  }

  findCartItem(key) {
    if (!key) return null;
    return this.querySelector(
      `.WI_cartDrawer_item[data-itemKey="${this.escapeAttr(key)}"]`
    );
  }

  pulseElement(el, className) {
    if (!el) return;
    el.classList.remove(className);
    void el.offsetWidth;
    el.classList.add(className);
    el.addEventListener(
      "animationend",
      () => el.classList.remove(className),
      { once: true }
    );
  }

  animateNewItems(container, addedKeys) {
    addedKeys.forEach((key, index) => {
      const el = container.querySelector(
        `.WI_cartDrawer_item[data-itemKey="${this.escapeAttr(key)}"]`
      );
      if (!el) return;
      el.classList.add("wi-cart-item--entering");
      el.style.transitionDelay = `${Math.min(index * 0.06, 0.24)}s`;
      requestAnimationFrame(() => {
        requestAnimationFrame(() => el.classList.add("wi-cart-item--entered"));
      });
      setTimeout(() => {
        el.classList.remove("wi-cart-item--entering", "wi-cart-item--entered");
        el.style.transitionDelay = "";
      }, 700);
    });
  }

  syncCartCount(container) {
    const countEl = container && container.querySelector("[data-cart-count]");
    if (!countEl) return;
    const n = countEl.textContent.trim();
    document.querySelectorAll(".global-cart-count").forEach((el) => {
      el.textContent = n;
    });
  }

  connectedCallback() {
    this.clickOncart();
    this.setupCartForms();
    window.refreshedCartDrawer = this.updateCart.bind(this);
  }

  clickOncart() {
    if (window.__wiCartEventsBound) return;
    window.__wiCartEventsBound = true;

    const refreshFromEvent = () => {
      const drawer = document.querySelector("wi-cartdrawer");
      if (!drawer) return;
      drawer.openCart({ refresh: true, mode: "add" });
    };
    document.addEventListener("opencart", refreshFromEvent);
    document.addEventListener("cart:refresh", refreshFromEvent);
  }

  openCart(options = {}) {
    const { refresh = false, mode = "refresh" } = options;
    const cartDrawer = this.querySelector(".WI_cartDrawerin");
    const cartDrawerUpsell = this.querySelector(".WI_cartDrawerin_upsell");
    this.style.display = "flex";
    this.classList.add("active");
    document.body.style.overflow = "hidden";
    setTimeout(() => {
      this.style.backgroundColor = "rgba(0,0,0,0.5)";
      if (cartDrawer) cartDrawer.style.transform = "translateX(0)";
      setTimeout(() => {
        if (cartDrawerUpsell)
          cartDrawerUpsell.classList.add("WI_cartDrawerin_upsell_active");
      }, 200);
    }, 10);

    if (refresh) {
      if (Date.now() - (this._lastUpdate || 0) < 600) {
        this.loadRecommendations();
      } else {
        this.setGlobalLoading(true);
        this.updateCart({ mode });
      }
    } else {
      this.loadRecommendations();
    }
  }

  closeCart(event) {
    if (event.target.closest(".WI_cartDrawerCls")) {
      this.closeCartdrawer();
    }
  }

  closeCartdrawer() {
    const cartDrawer = this.querySelector(".WI_cartDrawerin");
    const cartDrawerUpsell = this.querySelector(".WI_cartDrawerin_upsell");
    this.classList.remove("active");
    if (cartDrawerUpsell)
      cartDrawerUpsell.classList.remove("WI_cartDrawerin_upsell_active");
    document.body.style.overflow = "";
    setTimeout(() => {
      this.style.backgroundColor = "rgba(0,0,0,0)";
      if (cartDrawer) cartDrawer.style.transform = "translateX(100%)";
      setTimeout(() => {
        this.style.display = "none";
      }, 230);
    }, 10);
  }

  cartBgclick(event) {
    if (event.target === this) {
      this.closeCartdrawer();
    }
  }

  renderContents(parsedState) {
    const addedKey = parsedState?.items?.length
      ? parsedState.items[parsedState.items.length - 1].key
      : null;
    this._lastUpdate = 0;
    this.openCart({ refresh: false });
    this.setGlobalLoading(true);
    this.updateCart({ mode: "add", itemKey: addedKey });
  }

  updateCart(options = {}) {
    this._updateQueue = this._updateQueue.then(() =>
      this._performCartUpdate(options)
    );
    return this._updateQueue;
  }

  async _performCartUpdate(options = {}) {
    const { mode = "refresh", itemKey = null } = options;
    this._lastUpdate = Date.now();

    try {
      const currentCart = this.querySelector(".WI_cartDrawerin_cart");
      const oldKeys = this.getItemKeys(currentCart);
      const hadEmptyState = !!currentCart?.querySelector(
        ".WI_cartDrawerin_cart_empty"
      );

      if (mode === "remove" && itemKey) {
        const removingItem = this.findCartItem(itemKey);
        if (removingItem) {
          this.setItemLoading(removingItem, true);
          removingItem.classList.add("wi-cart-item--removing");
          await this.wait(420);
        }
      } else if (itemKey) {
        this.setItemLoading(this.findCartItem(itemKey), true);
      } else if (mode === "add" || mode === "refresh") {
        this.setGlobalLoading(true);
      }

      this.classList.add("wi-cart-updating");

      const res = await fetch(`${this.routesRoot()}?sections=cart-drawer`);
      if (!res.ok) throw new Error("Cart section fetch failed");
      const data = await res.json();
      const parsedHTML = new DOMParser().parseFromString(
        data["cart-drawer"],
        "text/html"
      );
      const newCartItems = parsedHTML.querySelector(".WI_cartDrawerin_cart");

      if (!newCartItems) {
        console.error("WIcartDrawer: cart section markup missing .WI_cartDrawerin_cart");
      }

      if (newCartItems && currentCart) {
        const newKeys = this.getItemKeys(newCartItems);
        const addedKeys = newKeys.filter((key) => !oldKeys.includes(key));
        const hasEmptyState = !!newCartItems.querySelector(
          ".WI_cartDrawerin_cart_empty"
        );

        currentCart.innerHTML = newCartItems.innerHTML;
        this.syncCartCount(currentCart);

        if (hadEmptyState && !hasEmptyState) {
          const body = currentCart.querySelector(".WI_cartDrawerin_cart_body");
          if (body) {
            body.classList.add("wi-cart-body--fade-in");
            body.addEventListener(
              "animationend",
              () => body.classList.remove("wi-cart-body--fade-in"),
              { once: true }
            );
          }
        }

        if (addedKeys.length) {
          this.animateNewItems(currentCart, addedKeys);
        }

        if (itemKey && (mode === "update" || mode === "add")) {
          const updatedItem = this.findCartItem(itemKey);
          if (updatedItem && !addedKeys.includes(itemKey)) {
            this.pulseElement(updatedItem, "wi-cart-item--updating");
          }
        }

        const countEl = currentCart.querySelector(".WI_cartDrawer_count");
        if (countEl && newKeys.length !== oldKeys.length) {
          this.pulseElement(countEl, "wi-cart-count--bump");
        }

        const total = currentCart.querySelector(".WI_cartDrawer_total_price");
        if (total) this.pulseElement(total, "wi-cart-total--pulse");
      }

      this._lastUpdate = Date.now();
      this.loadRecommendations();
    } catch (err) {
      console.error("WIcartDrawer Update Error:", err);
    } finally {
      this.classList.remove("wi-cart-updating");
      this.clearLoadingStates();
    }
  }

  loadRecommendations() {
    const dataEl = this.querySelector("#cart-drawer-data");
    const list = this.querySelector("#WI_upsell_list");
    if (!list) return;

    if (!dataEl) {
      list.innerHTML = "";
      return;
    }

    const firstProductId = dataEl.getAttribute("data-first-product-id");
    const cartHandlesAttr = dataEl.getAttribute("data-cart-handles");
    const cartHandles = cartHandlesAttr ? cartHandlesAttr.split(",") : [];

    if (!firstProductId) {
      list.innerHTML = "";
      return;
    }

    if (this._recsAbort) this._recsAbort.abort();
    this._recsAbort = new AbortController();
    const { signal } = this._recsAbort;
    const baseUrl = this.routesRoot();

    fetch(
      `${baseUrl}recommendations/products.json?product_id=${firstProductId}&limit=6&intent=related`,
      { signal }
    )
      .then((r) => r.json())
      .then((data) => {
        const prods = (data.products || []).filter(
          (p) => !cartHandles.includes(p.handle) && p.available
        );

        if (!prods.length) {
          list.innerHTML = "";
          return;
        }

        list.innerHTML = prods
          .slice(0, 5)
          .map((prod) => {
            const featured =
              typeof prod.featured_image === "object"
                ? prod.featured_image &&
                  (prod.featured_image.src || prod.featured_image.url)
                : prod.featured_image;
            const imgSrc = featured
              ? featured.replace(/(\?.*)?$/, "?width=160")
              : "";
            const variant = prod.variants && prod.variants[0];
            const variantId = variant ? variant.id : "";
            const compare =
              variant && variant.compare_at_price > variant.price
                ? variant.compare_at_price
                : 0;
            const priceHtml =
              compare > 0
                ? `<span class="WI_upsell_price--was">${this.formatMoney(
                    compare
                  )}</span><span class="WI_upsell_price--sale">${this.formatMoney(
                    prod.price
                  )}</span>`
                : `<span class="WI_upsell_price--reg">${this.formatMoney(
                    prod.price
                  )}</span>`;

            return `<div class="WI_upsell_item">
              <a href="${this.escapeHtml(prod.url)}" class="WI_upsell_img">
                <img src="${this.escapeHtml(imgSrc)}" alt="${this.escapeHtml(
                  prod.title
                )}" loading="lazy">
              </a>
              <div class="WI_upsell_info">
                <a href="${this.escapeHtml(
                  prod.url
                )}" class="WI_upsell_title_link">${this.escapeHtml(
                  prod.title
                )}</a>
                <div class="WI_upsell_prices">${priceHtml}</div>
              </div>
              <button type="button" class="WI_upsell_add_btn" data-variant-id="${variantId}" aria-label="Add ${this.escapeHtml(
                prod.title
              )}">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                  <path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/>
                  <path d="M3 6h18M16 10a4 4 0 0 1-8 0"/>
                </svg>
              </button>
            </div>`;
          })
          .join("");
      })
      .catch((err) => {
        if (err && err.name === "AbortError") return;
      });
  }

  async addUpsellAjax(variantId, btn) {
    if (!variantId || this.isProcessing) return;
    this.isProcessing = true;
    if (btn) btn.disabled = true;

    try {
      this.setGlobalLoading(true);
      const response = await fetch("/cart/add.js", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ items: [{ id: variantId, quantity: 1 }] }),
      });
      if (response.ok) {
        this._lastUpdate = 0;
        await this.updateCart({ mode: "add" });
      } else {
        this.clearLoadingStates();
      }
    } catch (err) {
      console.error("Upsell add error:", err);
      this.clearLoadingStates();
    } finally {
      if (btn) btn.disabled = false;
      this.isProcessing = false;
    }
  }

  async changeLineQuantity(key, newQuantity, mode, itemEl) {
    if (this.classList.contains("wi-cart-updating")) return;
    this.setItemLoading(itemEl, true);
    try {
      const res = await fetch("/cart/change.js", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ id: key, quantity: newQuantity }),
      });
      if (!res.ok) throw new Error("Cart change failed");
      await this.updateCart({ mode, itemKey: key });
    } catch (err) {
      console.error("WIcartDrawer quantity error:", err);
      this.clearLoadingStates();
    }
  }

  async incQuantity(event) {
    const btn = event.target.closest(".WI_cartDrawer_plus");
    if (!btn || !this.contains(btn)) return;
    const itemEl = btn.closest(".WI_cartDrawer_item");
    if (!itemEl) return;
    const keyID = itemEl.getAttribute("data-itemKey");
    const input = itemEl.querySelector(".WI_cartDrawer_quantity input");
    const newQuantity = Number(input && input.value) + 1;
    await this.changeLineQuantity(keyID, newQuantity, "update", itemEl);
  }

  async decQuantity(event) {
    const btn = event.target.closest(".WI_cartDrawer_minus");
    if (!btn || !this.contains(btn)) return;
    const itemEl = btn.closest(".WI_cartDrawer_item");
    if (!itemEl) return;
    const keyID = itemEl.getAttribute("data-itemKey");
    const input = itemEl.querySelector(".WI_cartDrawer_quantity input");
    const newQuantity = Number(input && input.value) - 1;
    if (newQuantity < 0) return;
    const updateMode = newQuantity === 0 ? "remove" : "update";
    await this.changeLineQuantity(keyID, newQuantity, updateMode, itemEl);
  }

  async revQuantity(event) {
    const btn = event.target.closest(".cartDrawerRemove");
    if (!btn || !this.contains(btn)) return;
    const itemEl = btn.closest(".WI_cartDrawer_item");
    if (!itemEl) return;
    const keyID = itemEl.getAttribute("data-itemKey");
    await this.changeLineQuantity(keyID, 0, "remove", itemEl);
  }

  setupCartForms() {
    if (window.__wiCartFormCapture) return;
    window.__wiCartFormCapture = true;
    document.addEventListener(
      "submit",
      async (e) => {
        const form = e.target;
        if (!(form instanceof HTMLFormElement)) return;
        const action = form.getAttribute("action") || form.action || "";
        if (!action.includes("/cart/add")) return;
        if (form.closest("product-form")) return;
        if (form.closest("wi-cartdrawer")) return;

        const drawer = document.querySelector("wi-cartdrawer");
        if (!drawer) return;

        e.preventDefault();
        e.stopImmediatePropagation();
        if (drawer.isProcessing) return;
        drawer.isProcessing = true;

        try {
          drawer.openCart();
          drawer.setGlobalLoading(true);
          const response = await fetch("/cart/add.js", {
            method: "POST",
            body: new FormData(form),
          });
          if (!response.ok) throw new Error("Failed to add to cart");
          drawer._lastUpdate = 0;
          await drawer.updateCart({ mode: "add" });
        } catch (error) {
          console.error("Error adding to cart:", error);
          drawer.clearLoadingStates();
        } finally {
          drawer.isProcessing = false;
        }
      },
      true
    );
  }

  handleCartClicks(event) {
    if (event.target.classList.contains("WI_discount_toggle")) {
      const wrap = this.querySelector(".WI_discount_wrap");
      if (wrap) wrap.classList.toggle("is-collapsed");
      return;
    }

    const upsellBtn = event.target.closest(".WI_upsell_add_btn");
    if (upsellBtn && this.contains(upsellBtn)) {
      const variantId = upsellBtn.getAttribute("data-variant-id");
      if (variantId) this.addUpsellAjax(Number(variantId), upsellBtn);
      return;
    }

    if (event.target.classList.contains("WI_discount_btn")) {
      const btn = event.target;
      const wrap = btn.closest(".WI_discount_wrap");
      if (wrap) {
        const input = wrap.querySelector(".WI_discount_input");
        if (input && input.value) {
          window.location.href =
            "/checkout?discount=" + encodeURIComponent(input.value);
        }
      }
    }
  }

  handleCartInputs(event) {
    if (event.target.classList.contains("WI_discount_input")) {
      const input = event.target;
      const form = input.closest("form");
      if (!form) return;
      let discountHidden = form.querySelector('input[type="hidden"][name="discount"]');
      if (!discountHidden) {
        discountHidden = document.createElement("input");
        discountHidden.type = "hidden";
        discountHidden.name = "discount";
        form.appendChild(discountHidden);
      }
      discountHidden.value = input.value;
    }
  }

  async handleCartSubmits(event) {
    /* reserved */
  }

  async addCompleteLookAjax() {
    /* removed — upsell uses addUpsellAjax */
  }
}

if (!customElements.get("wi-cartdrawer")) {
  customElements.define("wi-cartdrawer", WIcartDrawer);
}
