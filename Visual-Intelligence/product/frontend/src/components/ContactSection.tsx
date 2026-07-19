export function ContactSection() {
  return (
    <section className="relative w-full min-h-screen bg-black flex flex-col items-center justify-center py-32 px-6 z-[200]">
      <div className="relative z-10 w-full max-w-4xl mx-auto flex flex-col items-center">
        
        {/* Header */}
        <h2 className="text-[12px] tracking-[0.28em] font-medium opacity-70 mb-8 text-white uppercase text-center">
          Inquiries
        </h2>
        <h1 className="font-serif font-bold text-[56px] lg:text-[72px] leading-[0.95] text-center mb-24 max-w-2xl">
          Establish Connection.
        </h1>

        {/* Contact Form */}
        <form className="w-full max-w-2xl flex flex-col gap-12" onSubmit={(e) => e.preventDefault()}>
          
          {/* Input Group */}
          <div className="relative group">
            <input 
              type="text" 
              id="name"
              required
              className="w-full bg-transparent border-b border-white/20 pb-4 pt-2 text-[18px] text-white placeholder-transparent focus:outline-none focus:border-white transition-colors peer"
              placeholder="Name"
            />
            <label 
              htmlFor="name" 
              className="absolute left-0 top-2 text-[14px] text-white/50 tracking-widest uppercase transition-all peer-focus:-top-6 peer-focus:text-[11px] peer-focus:text-white peer-valid:-top-6 peer-valid:text-[11px] peer-valid:text-white/70 cursor-text"
            >
              Identification
            </label>
          </div>

          <div className="relative group">
            <input 
              type="email" 
              id="email"
              required
              className="w-full bg-transparent border-b border-white/20 pb-4 pt-2 text-[18px] text-white placeholder-transparent focus:outline-none focus:border-white transition-colors peer"
              placeholder="Email"
            />
            <label 
              htmlFor="email" 
              className="absolute left-0 top-2 text-[14px] text-white/50 tracking-widest uppercase transition-all peer-focus:-top-6 peer-focus:text-[11px] peer-focus:text-white peer-valid:-top-6 peer-valid:text-[11px] peer-valid:text-white/70 cursor-text"
            >
              Transmission Vector (Email)
            </label>
          </div>

          <div className="relative group">
            <textarea 
              id="message"
              required
              rows={4}
              className="w-full bg-transparent border-b border-white/20 pb-4 pt-2 text-[18px] text-white placeholder-transparent focus:outline-none focus:border-white transition-colors peer resize-none"
              placeholder="Message"
            />
            <label 
              htmlFor="message" 
              className="absolute left-0 top-2 text-[14px] text-white/50 tracking-widest uppercase transition-all peer-focus:-top-6 peer-focus:text-[11px] peer-focus:text-white peer-valid:-top-6 peer-valid:text-[11px] peer-valid:text-white/70 cursor-text"
            >
              Directive
            </label>
          </div>

          {/* Submit Button */}
          <div className="mt-8 flex justify-center">
            <button 
              type="submit"
              className="relative overflow-hidden group rounded-full border border-white/30 bg-white/5 px-16 py-5 hover:bg-white/10 transition-colors backdrop-blur-md"
            >
              {/* Sweeping Glare */}
              <div className="absolute top-0 bottom-0 left-0 w-24 bg-gradient-to-r from-transparent via-white/30 to-transparent skew-x-[-20deg] pointer-events-none -translate-x-[150%] group-hover:translate-x-[300%] transition-transform duration-700 ease-in-out" />
              
              <span className="relative z-10 text-[13px] tracking-[0.2em] uppercase font-medium">
                Transmit
              </span>
            </button>
          </div>

        </form>
      </div>
    </section>
  );
}
