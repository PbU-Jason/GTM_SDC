import { getPermalink, getBlogPermalink } from './utils/permalinks';

export const headerData = {
  links: [
    {
      text: 'Home',
      href: getPermalink('/#'),
    },
    {
      text: '中文首頁',
      href: getPermalink('/mandarin'),
    },
    {
      text: 'Article',
      links: [
        {
          text: 'Science',
          href: getPermalink('science', 'post'),
        },
        {
          text: 'Instrument',
          href: getPermalink('instrument', 'post'),
        },
      ],
    },
    {
      text: 'Publication',
      href: getPermalink('/paper'),
    },
    {
      text: 'Data',
      links: [
        {
          text: 'Format',
          href: getPermalink('/format'),
        },
        {
          text: 'Catalog',
          href: 'https://crab0.astr.nthu.edu.tw/tt/'
        },
        {
          text: 'Product',
          href: 'https://crab0.astr.nthu.edu.tw/gtm_product/'
        },
      ],
    },
    {
      text: 'Team',
      href: getPermalink('/team'),
    },
  ],
};

export const footerData = {
  footNote: `
  © GTM - All rights reserved. Revised by Astro free template
  `,
};

