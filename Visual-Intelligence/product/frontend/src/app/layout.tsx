import type { Metadata } from "next";
import localFont from "next/font/local";
import { Cormorant_Garamond } from "next/font/google";
import "./globals.css";

const cormorantGaramond = Cormorant_Garamond({
  variable: "--font-cormorant-garamond",
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  style: ["normal", "italic"],
});

const neueHaas = localFont({
  src: [
    {
      path: "../../public/fonts/neuehaasgrottext-55roman-trial.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "../../public/fonts/neuehaasgrottext-65medium-trial.otf",
      weight: "500",
      style: "normal",
    },
    {
      path: "../../public/fonts/neuehaasgrottext-75bold-trial.otf",
      weight: "700",
      style: "normal",
    }
  ],
  variable: "--font-neue-haas",
});

const butler = localFont({
  src: [
    {
      path: "../../public/fonts/Butler-Free-Rmn.otf",
      weight: "400",
      style: "normal",
    },
    {
      path: "../../public/fonts/Butler-Free-Med.otf",
      weight: "500",
      style: "normal",
    },
    {
      path: "../../public/fonts/Butler-Free-Bd.otf",
      weight: "700",
      style: "normal",
    },
  ],
  variable: "--font-butler",
});

export const metadata: Metadata = {
  title: "Creative Intelligence Institute",
  description: "Where Creativity Becomes Intelligence",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${neueHaas.variable} ${cormorantGaramond.variable} ${butler.variable}`}>
      <body className={`font-sans font-medium antialiased`}>
        {children}
        <div className="film-grain" />
      </body>
    </html>
  );
}
