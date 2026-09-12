import { AgentId, ChatMessage } from "./types";

interface MockOrchestratorOptions {
  prompt: string;
  onTyping: (agentId: AgentId | null) => void;
  onMessage: (msg: ChatMessage) => void;
  onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void;
  onTriggerApproval?: () => void;
}

export class MockOrchestrator {
  private static getTime(): string {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  static async processUserPrompt(options: MockOrchestratorOptions): Promise<void> {
    const { prompt, onTyping, onMessage, onTaskUpdate, onTriggerApproval } = options;
    const lower = prompt.toLowerCase();

    // Department level mentions
    const isDeptStrategy = lower.includes("@strategy");
    const isDeptCreative = lower.includes("@creative");
    const isDeptIntelligence = lower.includes("@intelligence");
    const isDeptContent = lower.includes("@content");
    const isDeptQuality = lower.includes("@quality");

    // Specific agent handle mentions
    const isMaterialMentioned = lower.includes("@material-dna");
    const isVisualMentioned = lower.includes("@visual-dna") || lower.includes("@visual_dna_analyst_01");
    const isArtMentioned = lower.includes("@art-director") || lower.includes("@art_director_01") || lower.includes("@creative_director_01");
    const isStrategistMentioned = lower.includes("@campaign-strategist") || lower.includes("@campaign_strategist_01") || lower.includes("@brand_strategist_01");
    const isBrandMentioned = lower.includes("@brand-dna");
    const isTrendMentioned = lower.includes("@trend_researcher_01");
    const isCriticMentioned = lower.includes("@creative_critic_01") || lower.includes("@independent_reviewer_01");
    const isRendererMentioned = lower.includes("@synthesizer");
    const isValidatorMentioned = lower.includes("@quality-validator");
    const isCopywriterMentioned = lower.includes("@creative-copywriter") || lower.includes("@copywriter_01") || lower.includes("@scriptwriter_01");

    const hasSpecificMention =
      isDeptStrategy ||
      isDeptCreative ||
      isDeptIntelligence ||
      isDeptContent ||
      isDeptQuality ||
      isMaterialMentioned ||
      isVisualMentioned ||
      isArtMentioned ||
      isStrategistMentioned ||
      isBrandMentioned ||
      isTrendMentioned ||
      isCriticMentioned ||
      isRendererMentioned ||
      isValidatorMentioned ||
      isCopywriterMentioned;

    // SCENARIO 1: SPECIFIC DEPARTMENT OR AGENT TAGGED
    if (hasSpecificMention) {
      if (isDeptStrategy || isBrandMentioned || isStrategistMentioned) {
        await this.runBrandDnaAgent(onTyping, onMessage, onTaskUpdate, prompt);
      }
      if (isDeptIntelligence || isMaterialMentioned || isTrendMentioned) {
        await this.runMaterialDnaAgent(onTyping, onMessage, onTaskUpdate, prompt);
      }
      if (isDeptIntelligence || isVisualMentioned) {
        await this.runVisualDnaAgent(onTyping, onMessage, onTaskUpdate, prompt);
      }
      if (isDeptCreative || isArtMentioned) {
        await this.runArtDirectorAgent(onTyping, onMessage, onTaskUpdate, prompt, onTriggerApproval);
      }
      if (isDeptContent || isCopywriterMentioned) {
        await this.runCopywriterAgent(onTyping, onMessage, onTaskUpdate);
      }
      if (isDeptQuality || isValidatorMentioned || isCriticMentioned) {
        await this.runValidatorAgent(onTyping, onMessage, onTaskUpdate);
      }
      if (isRendererMentioned) {
        await this.runSynthesizerAgent(onTyping, onMessage, onTaskUpdate);
      }
      return;
    }

    // SCENARIO 2: GOVERNED 5-PHASE PIPELINE CASCADE
    // Phase 1: Strategy Department (Brand & Campaign Positioning)
    await this.runBrandDnaAgent(onTyping, onMessage, onTaskUpdate, prompt);
    
    // Phase 2: Intelligence Department (Trend & Visual DNA Extraction)
    await this.runMaterialDnaAgent(onTyping, onMessage, onTaskUpdate, prompt);
    await this.runVisualDnaAgent(onTyping, onMessage, onTaskUpdate, prompt);

    // Phase 3: Creative Department (Art & Creative Directives - triggers approval gate)
    await this.runArtDirectorAgent(onTyping, onMessage, onTaskUpdate, prompt, onTriggerApproval);
  }

  // --- AGENT RUNNERS ---

  private static async runBrandDnaAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void,
    prompt: string
  ) {
    onTaskUpdate("brand-dna", "processing", "Validating Brand Guard Constraints");
    onTyping("brand-dna");
    await this.delay(1400);

    onMessage({
      id: Date.now().toString(),
      sender: "brand-dna",
      senderName: "@Brand-DNA",
      time: this.getTime(),
      text: `Brand alignment verified for: "${prompt.slice(0, 40)}...". Scoped archetype [Luxury / Minimalist] and architectural tone tokens passed down to team nodes.`,
    });

    onTaskUpdate("brand-dna", "completed", "Brand Alignment Locked");
    onTyping(null);
  }

  private static async runMaterialDnaAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void,
    prompt: string
  ) {
    onTaskUpdate("material-dna", "processing", "Analyzing Textile Micro-Structures");
    onTyping("material-dna");
    await this.delay(1600);

    onMessage({
      id: Date.now().toString(),
      sender: "material-dna",
      senderName: "@Material-DNA",
      time: this.getTime(),
      text: `Analyzed specimen properties based on directive. Formulated fabric DNA specification:`,
      dnaCard: {
        title: "FABRIC DNA SPECIFICATION: Banarasi Zari Silk",
        details: {
          "Weave Class": "Handloom Brocade",
          "Warp Threads": "Pure Silk 120 GSM",
          "Weft Threads": "Real Metallic Zari",
          "Drape Weight": "Architectural Heavy",
        },
        bullet: "High specular reflectivity on metallic zari. Recommend directional backlight to preserve luster contrast.",
      },
    });

    onTaskUpdate("material-dna", "completed", "Textile DNA Spec Ready");
    onTyping(null);
  }

  private static async runVisualDnaAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void,
    prompt: string
  ) {
    onTaskUpdate("image-decomposer", "processing", "Deconstructing Reference Lighting & Perspective");
    onTyping("image-decomposer");
    await this.delay(1800);

    onMessage({
      id: Date.now().toString(),
      sender: "image-decomposer",
      senderName: "@Visual-DNA",
      time: this.getTime(),
      text: `Deconstructed visual reference framing into 3 core photographic components:`,
      photoCard: {
        title: "PHOTOGRAPHIC DECOMPOSITION",
        description: "Deconstructed architectural perspective from mood inputs.",
        images: [
          { label: "Perspective", url: "Heritage fort colonnade / 35mm wide angle" },
          { label: "Lighting", url: "Directional side backlight / 5600K key wrap" },
          { label: "Composition", url: "Golden spiral subject placement with shadow void" },
        ],
      },
    });

    onTaskUpdate("image-decomposer", "completed", "Photographic Decomposition Ready");
    onTyping(null);
  }

  private static async runArtDirectorAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void,
    prompt: string,
    onTriggerApproval?: () => void
  ) {
    onTaskUpdate("art-director", "processing", "Resolving Composition & Shot Directives");
    onTyping("art-director");
    await this.delay(1600);

    onMessage({
      id: Date.now().toString(),
      sender: "art-director",
      senderName: "@Art-Director",
      time: this.getTime(),
      text: `Resolved shot directives combining Textile DNA and Visual Reference properties. Awaiting approval to synthesize:`,
      dnaCard: {
        title: "ART DIRECTION DIRECTIVE",
        details: {
          "Location": "Heritage Corridor at Twilight",
          "Pose & Flow": "Static Geometrical Placement",
          "Aspect Ratio": "3:4 Editorial",
          "Color Grade": "Obsidian & Gold Contrast",
        },
        bullet: "All parameters bound to VYREN Atelier brand profile. Click 'Approve & Render' to execute image synthesis.",
      },
    });

    onTaskUpdate("art-director", "completed", "Shot Setup Directives Complete");
    onTyping(null);

    if (onTriggerApproval) {
      onTriggerApproval();
    }
  }

  private static async runStrategistAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void,
    prompt: string
  ) {
    onTaskUpdate("strategist", "processing", "Outlining Shot Sequence Strategy");
    onTyping("strategist");
    await this.delay(1400);

    onMessage({
      id: Date.now().toString(),
      sender: "strategist",
      senderName: "@Campaign-Strategist",
      time: this.getTime(),
      text: `Campaign sequence planned: 4 key visual touchpoints mapped (Hero Portrait, Macro Weave Detail, Full Silhouette, Motion Swatch).`,
    });

    onTaskUpdate("strategist", "completed", "Sequence Strategy Outlined");
    onTyping(null);
  }

  // --- RENDERING PIPELINE (Triggered upon clicking Approve & Render) ---

  static async runRenderingPipeline(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void
  ): Promise<void> {
    // 1. @Synthesizer
    await this.runSynthesizerAgent(onTyping, onMessage, onTaskUpdate);

    // 2. @Quality-Validator
    await this.runValidatorAgent(onTyping, onMessage, onTaskUpdate);

    // 3. @Creative-Copywriter
    await this.runCopywriterAgent(onTyping, onMessage, onTaskUpdate);
  }

  private static async runSynthesizerAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void
  ) {
    onTaskUpdate("renderer", "processing", "Synthesizing High-Fidelity Campaign Assets");
    onTyping("renderer");
    await this.delay(2200);

    onMessage({
      id: Date.now().toString(),
      sender: "renderer",
      senderName: "@Synthesizer",
      time: this.getTime(),
      text: `Successfully synthesized 2 high-fidelity visual assets based on the approved shot directives.`,
    });

    const sampleImages = [
      "https://images.unsplash.com/photo-1610030469983-98e550d6193c?q=80&w=600",
      "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=600",
    ];

    for (let i = 0; i < sampleImages.length; i++) {
      onMessage({
        id: (Date.now() + i + 1).toString(),
        sender: "renderer",
        senderName: "@Synthesizer",
        time: this.getTime(),
        imageCard: {
          url: sampleImages[i],
          prompt: `Banarasi silk brocade saree shot in heritage corridor at twilight, dramatic lighting, aspect ratio 3:4, asset ${i + 1}`,
        },
      });
    }

    onTaskUpdate("renderer", "completed", "2 Campaign Assets Synthesized");
    onTyping(null);
  }

  private static async runValidatorAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void
  ) {
    onTaskUpdate("validator", "processing", "Verifying Physics & Drape Consistency");
    onTyping("validator");
    await this.delay(1500);

    onMessage({
      id: Date.now().toString(),
      sender: "validator",
      senderName: "@Quality-Validator",
      time: this.getTime(),
      text: `Quality review completed. Verified zari weave distortion, shadow continuity, and specular highlight preservation.`,
      qualityCard: {
        status: "PASSED",
        actions: ["Download Spec Sheet", "Inspect Weave Grid"],
      },
    });

    onTaskUpdate("validator", "completed", "Quality Review PASSED");
    onTyping(null);
  }

  private static async runCopywriterAgent(
    onTyping: (agentId: AgentId | null) => void,
    onMessage: (msg: ChatMessage) => void,
    onTaskUpdate: (agentId: AgentId, status: "idle" | "processing" | "completed", taskName?: string) => void
  ) {
    onTaskUpdate("copywriter", "processing", "Drafting Campaign Title & Editorial Copy");
    onTyping("copywriter");
    await this.delay(1400);

    onMessage({
      id: Date.now().toString(),
      sender: "copywriter",
      senderName: "@Creative-Copywriter",
      time: this.getTime(),
      text: `Drafted launch title and editorial narrative for the campaign:\n\n**'THE PALACE WEAVE'**\n*Where ancient Zari threads meet the soft shadows of history.*`,
    });

    onTaskUpdate("copywriter", "completed", "Editorial Narrative Drafted");
    onTyping(null);
  }

  private static delay(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
