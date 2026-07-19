export function Footer() {
  return (
    <footer className="relative w-full bg-black text-white pt-32 pb-16 px-6 border-t border-white/5 z-[200]">
      <div className="w-full max-w-7xl mx-auto flex flex-col items-center">
        
        {/* Navigation Links */}
        <div className="flex flex-wrap justify-center gap-12 mb-32">
          {['Intelligence', 'Architecture', 'Pricing', 'Documentation', 'Contact'].map((link) => (
            <a 
              key={link}
              href="#"
              className="text-[12px] tracking-[0.2em] font-medium uppercase opacity-50 hover:opacity-100 hover:text-[#E1D4C0] transition-all duration-300 relative group"
            >
              {link}
              {/* Underline scale effect */}
              <span className="absolute -bottom-2 left-0 w-full h-[1px] bg-[#E1D4C0] scale-x-0 group-hover:scale-x-100 transition-transform duration-500 origin-left" />
            </a>
          ))}
        </div>

        {/* Monumental Logomark */}
        <div className="w-full border-t border-white/10 pt-16 flex flex-col md:flex-row items-center justify-between gap-8">
          <p className="text-[11px] tracking-[0.1em] opacity-40 uppercase">
            © {new Date().getFullYear()} Atelier OS. All rights reserved.
          </p>
          
          <h2 className="font-serif font-bold text-[40px] md:text-[64px] leading-none tracking-tight">
            Atelier.
          </h2>

          <div className="flex items-center gap-6">
            <a href="#" className="text-[11px] tracking-[0.1em] opacity-40 hover:opacity-100 uppercase transition-opacity">Privacy</a>
            <a href="#" className="text-[11px] tracking-[0.1em] opacity-40 hover:opacity-100 uppercase transition-opacity">Terms</a>
          </div>
        </div>

      </div>
    </footer>
  );
}
