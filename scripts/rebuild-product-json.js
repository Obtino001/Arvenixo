const fs = require('fs');
const path = 'templates/product.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));
const main = data.sections.main;

if (main && main.settings) {
  main.settings['padding-block-start'] = 24;
  main.settings['padding-block-end'] = 40;
}

const cardBlocks = {
  gallery: {
    type: '_product-card-gallery',
    settings: { image_ratio: 'square', border: 'none', border_radius: 8 },
  },
  title: {
    type: 'product-title',
    settings: {
      type_preset: 'custom',
      font: 'var(--font-heading--family)',
      font_size: '1rem',
      color: 'var(--color-foreground-heading)',
      width: 'fit-content',
    },
  },
  price: {
    type: 'price',
    settings: {
      show_sale_price_first: true,
      type_preset: 'h6',
      width: '100%',
      alignment: 'left',
    },
  },
};

data.sections = {
  main,
  pdp_trust: {
    type: 'icons-with-text',
    blocks: {
      b1: {
        type: 'badge',
        settings: {
          title: 'Free standard shipping',
          text: 'On every order · arrives in 7–10 business days after shipping.',
        },
      },
      b2: {
        type: 'badge',
        settings: {
          title: 'Secure checkout',
          text: 'Encrypted payments with Shop Pay and major cards.',
        },
      },
      b3: {
        type: 'badge',
        settings: {
          title: '30-day returns',
          text: 'Eligible items · defective or incorrect orders always covered.',
        },
      },
      b4: {
        type: 'badge',
        settings: {
          title: 'Support that replies',
          text: 'Email support@arvenixo.com · typically 1–2 business days.',
        },
      },
    },
    block_order: ['b1', 'b2', 'b3', 'b4'],
    settings: {
      bg_color: '#f7f5f1',
      margin_top: 0,
      margin_bottom: 0,
      padding_top: 40,
      padding_bottom: 40,
    },
  },
  pdp_why: {
    type: 'section',
    blocks: {
      heading: {
        type: 'text',
        settings: {
          text: '<p>Why shoppers choose Arvenixo</p>',
          type_preset: 'h3',
          width: 'fit-content',
          max_width: 'narrow',
        },
      },
      copy: {
        type: 'text',
        settings: {
          text: '<p>Clear product details, free standard shipping, and a buy box built for confidence — so you know what you’re getting before you checkout.</p>',
          type_preset: 'rte',
          width: 'fit-content',
          max_width: 'normal',
        },
      },
      accordion: {
        type: 'accordion',
        settings: { icon: 'caret', dividers: true, type_preset: 'h5' },
        blocks: {
          r1: {
            type: '_accordion-row',
            settings: { heading: 'Everyday-ready materials & fit', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>Cases and devices are selected for daily use — precise cutouts, MagSafe-ready options, and clear model selection on the product page.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
          r2: {
            type: '_accordion-row',
            settings: { heading: 'Shipping & tracking included', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>Free standard shipping on all orders. Estimated delivery is 7–10 business days after your order ships, with tracking by email.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
          r3: {
            type: '_accordion-row',
            settings: { heading: 'Returns with clear rules', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>30-day return window on eligible items. Beauty devices may have hygiene restrictions once opened — damaged or incorrect items are always covered.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
        },
        block_order: ['r1', 'r2', 'r3'],
      },
    },
    block_order: ['heading', 'copy', 'accordion'],
    settings: {
      content_direction: 'column',
      gap: 20,
      section_width: 'page-width',
      color_scheme: 'scheme-1',
      'padding-block-start': 48,
      'padding-block-end': 24,
    },
  },
  pdp_howto: {
    type: 'section',
    blocks: {
      left: {
        type: 'group',
        settings: {
          content_direction: 'column',
          gap: 14,
          width: 'custom',
          custom_width: 100,
          vertical_alignment: 'center',
        },
        blocks: {
          h: {
            type: 'text',
            settings: {
              text: '<p>How to order with confidence</p>',
              type_preset: 'h3',
              width: 'fit-content',
            },
          },
          p: {
            type: 'text',
            settings: {
              text: '<ol><li>Choose your exact model, color, or option.</li><li>Add to cart — free shipping applies automatically.</li><li>Checkout securely with Shop Pay or card.</li><li>Track your package when it ships.</li></ol>',
              type_preset: 'rte',
              width: 'fit-content',
              max_width: 'normal',
            },
          },
          btn: {
            type: 'button',
            settings: {
              label: 'Contact support',
              link: 'shopify://pages/contact',
              style_class: 'button-secondary',
            },
          },
        },
        block_order: ['h', 'p', 'btn'],
      },
      right: {
        type: 'group',
        settings: {
          content_direction: 'column',
          gap: 14,
          width: 'custom',
          custom_width: 100,
          vertical_alignment: 'center',
          'padding-block-start': 24,
          'padding-block-end': 24,
          'padding-inline-start': 24,
          'padding-inline-end': 24,
        },
        blocks: {
          h: {
            type: 'text',
            settings: {
              text: '<p>What’s in the box</p>',
              type_preset: 'h4',
              width: 'fit-content',
            },
          },
          p: {
            type: 'text',
            settings: {
              text: '<p>Each product page lists inclusions (device/case, cable, or manual when applicable). Always check the description for your exact SKU before purchase.</p>',
              type_preset: 'rte',
              width: 'fit-content',
            },
          },
        },
        block_order: ['h', 'p'],
      },
    },
    block_order: ['left', 'right'],
    settings: {
      content_direction: 'row',
      vertical_on_mobile: true,
      gap: 32,
      section_width: 'page-width',
      color_scheme: 'scheme-1',
      'padding-block-start': 24,
      'padding-block-end': 48,
    },
  },
  pdp_faq: {
    type: 'section',
    blocks: {
      heading: {
        type: 'text',
        settings: {
          text: '<p>Product FAQ</p>',
          type_preset: 'h3',
          width: 'fit-content',
        },
      },
      accordion: {
        type: 'accordion',
        settings: { icon: 'caret', dividers: true, type_preset: 'h5' },
        blocks: {
          r1: {
            type: '_accordion-row',
            settings: { heading: 'Will this fit my iPhone model?', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>Select your exact model on this page before adding to cart. Confirm under Settings → General → About on your phone if you’re unsure.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
          r2: {
            type: '_accordion-row',
            settings: { heading: 'Is MagSafe charging supported?', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>MagSafe-compatible cases are labeled in the title or description. Always verify MagSafe wording on the specific product you’re buying.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
          r3: {
            type: '_accordion-row',
            settings: { heading: 'Can I return a beauty device?', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>Unopened beauty devices may be returned within 30 days. Opened personal-care items usually aren’t eligible for hygiene reasons unless damaged, defective, or incorrect.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
          r4: {
            type: '_accordion-row',
            settings: { heading: 'When will I get tracking?', icon: 'none' },
            blocks: {
              t: {
                type: 'text',
                settings: {
                  text: '<p>Tracking details are emailed when your order ships. Delivery estimates are 7–10 business days after shipping.</p>',
                  type_preset: 'rte',
                  width: '100%',
                },
              },
            },
            block_order: ['t'],
          },
        },
        block_order: ['r1', 'r2', 'r3', 'r4'],
      },
    },
    block_order: ['heading', 'accordion'],
    settings: {
      content_direction: 'column',
      gap: 20,
      section_width: 'page-width',
      color_scheme: 'scheme-1',
      'padding-block-start': 24,
      'padding-block-end': 48,
    },
  },
  pdp_recs: {
    type: 'product-recommendations',
    blocks: {
      'static-header': {
        type: '_product-list-content',
        name: 'Header',
        static: true,
        settings: {
          content_direction: 'row',
          horizontal_alignment: 'space-between',
          vertical_alignment: 'flex-end',
          gap: 12,
          width: 'fill',
        },
        blocks: {
          title: {
            type: '_product-list-text',
            settings: {
              text: '<h3>You may also like</h3>',
              type_preset: 'h3',
              width: 'fit-content',
            },
          },
        },
        block_order: ['title'],
      },
      'static-product-card': {
        type: '_product-card',
        name: 'Product card',
        static: true,
        settings: {
          product_card_gap: 4,
          inherit_color_scheme: true,
          border: 'none',
        },
        blocks: {
          'card-gallery': cardBlocks.gallery,
          'product-title': cardBlocks.title,
          price: cardBlocks.price,
        },
        block_order: ['card-gallery', 'product-title', 'price'],
      },
    },
    settings: {
      recommendation_type: 'related',
      layout_type: 'grid',
      carousel_on_mobile: true,
      max_products: 4,
      columns: 4,
      mobile_columns: '2',
      columns_gap: 16,
      rows_gap: 24,
      section_width: 'page-width',
      gap: 28,
      color_scheme: 'scheme-1',
      'padding-block-start': 32,
      'padding-block-end': 48,
    },
  },
  pdp_reviews_head: {
    type: 'section',
    blocks: {
      h: {
        type: 'text',
        settings: {
          text: '<p>Customer stories</p>',
          type_preset: 'h3',
          width: 'fit-content',
          alignment: 'center',
        },
      },
      p: {
        type: 'text',
        settings: {
          text: '<p>Real feedback helps other shoppers decide. Reviews appear here as customers share their experience.</p>',
          type_preset: 'rte',
          width: 'fit-content',
          max_width: 'normal',
          alignment: 'center',
        },
      },
    },
    block_order: ['h', 'p'],
    settings: {
      content_direction: 'column',
      horizontal_alignment_flex_direction_column: 'center',
      gap: 8,
      section_width: 'page-width',
      color_scheme: 'scheme-1',
      'padding-block-start': 24,
      'padding-block-end': 8,
    },
  },
  pdp_testimonials: {
    type: 'testimonial',
    blocks: {
      t1: {
        type: 'testimonial',
        settings: {
          review_text:
            'Fast shipping update and the case fit perfectly. MagSafe hold feels strong in daily use.',
          customer_name: 'Alex M.',
        },
      },
      t2: {
        type: 'testimonial',
        settings: {
          review_text:
            'Checkout was simple and tracking arrived when the order shipped. Packaging was clean and secure.',
          customer_name: 'Jordan K.',
        },
      },
      t3: {
        type: 'testimonial',
        settings: {
          review_text:
            'Support answered my model question quickly. Happy with the quality for the price.',
          customer_name: 'Sam R.',
        },
      },
    },
    block_order: ['t1', 't2', 't3'],
    settings: {
      heading: '',
      subheading: '',
      bg_color: 'rgba(0,0,0,0)',
      margin_top: 0,
      margin_bottom: 0,
      padding_top: 8,
      padding_bottom: 48,
    },
  },
  pdp_more: {
    type: 'featured-collection',
    blocks: {
      'static-product-card': {
        type: '_product-card',
        static: true,
        settings: {
          product_card_gap: 0,
          inherit_color_scheme: true,
          border: 'none',
        },
        blocks: {
          gallery: cardBlocks.gallery,
          title: cardBlocks.title,
          price: cardBlocks.price,
          buy: {
            type: 'buy-buttons',
            settings: { stacking: false, show_pickup_availability: false },
            blocks: {
              quantity: { type: 'quantity', disabled: true, static: true, settings: {} },
              'add-to-cart': {
                type: 'add-to-cart',
                static: true,
                settings: { style_class: 'button' },
              },
              'accelerated-checkout': {
                type: 'accelerated-checkout',
                disabled: true,
                static: true,
                settings: {},
              },
            },
            block_order: [],
          },
        },
        block_order: ['gallery', 'title', 'price', 'buy'],
      },
    },
    settings: {
      collection: 'all',
      block_heading: 'More from Arvenixo',
      enable_autoplay: false,
      desktop_slides: 4,
      desktop_spacing: 16,
      desktop_arrows: true,
      desktop_progress_bar: false,
      tablet_slides: 3,
      mobile_slides: 1.6,
      mobile_spacing: 12,
      mobile_arrows: true,
      mobile_progress_bar: false,
    },
  },
};

data.order = [
  'main',
  'pdp_trust',
  'pdp_why',
  'pdp_howto',
  'pdp_faq',
  'pdp_recs',
  'pdp_reviews_head',
  'pdp_testimonials',
  'pdp_more',
];

fs.writeFileSync(path, JSON.stringify(data));
console.log('product.json rebuilt', data.order.length, 'sections');
