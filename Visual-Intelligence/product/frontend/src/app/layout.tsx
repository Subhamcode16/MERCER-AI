import type { Metadata } from "next";
import localFont from "next/font/local";
import { Cormorant_Garamond } from "next/font/google";
import { AuthProvider } from "@/contexts/AuthContext";
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

const nohemi = localFont({
  src: [
    {
      path: "../../public/fonts/Nohemi-Thin.woff2",
      weight: "100",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-ExtraLight.woff2",
      weight: "200",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-Light.woff2",
      weight: "300",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-Regular.woff2",
      weight: "400",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-Medium.woff2",
      weight: "500",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-SemiBold.woff2",
      weight: "600",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-Bold.woff2",
      weight: "700",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-ExtraBold.woff2",
      weight: "800",
      style: "normal",
    },
    {
      path: "../../public/fonts/Nohemi-Black.woff2",
      weight: "900",
      style: "normal",
    },
  ],
  variable: "--font-nohemi",
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
    <html lang="en" suppressHydrationWarning className={`${neueHaas.variable} ${cormorantGaramond.variable} ${butler.variable} ${nohemi.variable}`}>
      <body suppressHydrationWarning className={`font-sans font-medium antialiased`}>
        <AuthProvider>
          {children}
          <div className="film-grain" />
        </AuthProvider>
      </body>
    </html>
  );
}
