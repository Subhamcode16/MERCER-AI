"use client";

import React, { useEffect, useRef } from "react";
import * as THREE from "three";

export const MeadowBackground: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<{
    renderer: THREE.WebGLRenderer;
    animId: number;
    dispose: () => void;
  } | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;

    // --- Procedural Canvas Textures ---
    function makeGroundTexture(renderer: THREE.WebGLRenderer) {
      const S = 512;
      const c = document.createElement("canvas");
      c.width = c.height = S;
      const ctx = c.getContext("2d")!;
      ctx.fillStyle = "#8aa25a";
      ctx.fillRect(0, 0, S, S);

      for (let i = 0; i < 60; i++) {
        const x = Math.random() * S, y = Math.random() * S, r = 30 + Math.random() * 80;
        const g = ctx.createRadialGradient(x, y, 0, x, y, r);
        const warm = Math.random() < 0.5;
        g.addColorStop(0, warm ? "rgba(130,140,60,0.25)" : "rgba(60,95,45,0.3)");
        g.addColorStop(1, "rgba(0,0,0,0)");
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fill();
      }

      const wrapStroke = (x: number, y: number, len: number, w: number, col: string) => {
        ctx.strokeStyle = col;
        ctx.lineWidth = w;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + (Math.random() - 0.5) * 3, y - len);
        ctx.stroke();

        for (const dx of [-S, 0, S]) {
          for (const dy of [-S, 0, S]) {
            if (dx === 0 && dy === 0) continue;
            if (x + dx > -10 && x + dx < S + 10 && y + dy > -10 && y + dy < S + 10) {
              ctx.beginPath();
              ctx.moveTo(x + dx, y + dy);
              ctx.lineTo(x + dx + (Math.random() - 0.5) * 3, y + dy - len);
              ctx.stroke();
            }
          }
        }
      };

      for (let i = 0; i < 2600; i++) {
        const light = Math.random() < 0.5;
        wrapStroke(
          Math.random() * S,
          Math.random() * S,
          4 + Math.random() * 10,
          1 + Math.random() * 1.5,
          light ? `rgba(150,170,80,${0.12 + Math.random() * 0.2})` : `rgba(35,60,25,${0.12 + Math.random() * 0.2})`
        );
      }

      for (let i = 0; i < 300; i++) {
        wrapStroke(
          Math.random() * S,
          Math.random() * S,
          3 + Math.random() * 6,
          1,
          `rgba(190,170,90,${0.08 + Math.random() * 0.12})`
        );
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.colorSpace = THREE.SRGBColorSpace;
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      return tex;
    }

    function makeGroundBump(renderer: THREE.WebGLRenderer) {
      const S = 512;
      const c = document.createElement("canvas");
      c.width = c.height = S;
      const ctx = c.getContext("2d")!;
      ctx.fillStyle = "#888888";
      ctx.fillRect(0, 0, S, S);

      const wrapStroke = (x: number, y: number, len: number, w: number, col: string) => {
        ctx.strokeStyle = col;
        ctx.lineWidth = w;
        ctx.lineCap = "round";
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x + (Math.random() - 0.5) * 3, y - len);
        ctx.stroke();
        for (const dx of [-S, 0, S]) {
          for (const dy of [-S, 0, S]) {
            if (dx === 0 && dy === 0) continue;
            if (x + dx > -10 && x + dx < S + 10 && y + dy > -10 && y + dy < S + 10) {
              ctx.beginPath();
              ctx.moveTo(x + dx, y + dy);
              ctx.lineTo(x + dx + (Math.random() - 0.5) * 3, y + dy - len);
              ctx.stroke();
            }
          }
        }
      };

      for (let i = 0; i < 2600; i++) {
        const light = Math.random() < 0.5;
        wrapStroke(
          Math.random() * S,
          Math.random() * S,
          4 + Math.random() * 10,
          1 + Math.random() * 1.5,
          light ? `rgba(190,190,190,${0.12 + Math.random() * 0.2})` : `rgba(70,70,70,${0.12 + Math.random() * 0.2})`
        );
      }

      const tex = new THREE.CanvasTexture(c);
      tex.wrapS = tex.wrapT = THREE.RepeatWrapping;
      tex.anisotropy = renderer.capabilities.getMaxAnisotropy();
      return tex;
    }

    function makeFlowerTexture(color: string, heart: string) {
      const S = 128;
      const c = document.createElement("canvas");
      c.width = c.height = S;
      const ctx = c.getContext("2d")!;
      ctx.clearRect(0, 0, S, S);
      const petals = 6 + (Math.random() * 3 | 0);
      for (let p = 0; p < petals; p++) {
        const a = (p / petals) * Math.PI * 2 + Math.random() * 0.3;
        const d = S * (0.22 + Math.random() * 0.06);
        const px = S / 2 + Math.cos(a) * d, py = S / 2 + Math.sin(a) * d;
        const g = ctx.createRadialGradient(px, py, 1, px, py, S * 0.2);
        g.addColorStop(0, color + "ff");
        g.addColorStop(1, color + "00");
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.arc(px, py, S * 0.2, 0, Math.PI * 2);
        ctx.fill();
      }
      const hg = ctx.createRadialGradient(S / 2, S / 2, 1, S / 2, S / 2, S * 0.13);
      hg.addColorStop(0, heart + "ff");
      hg.addColorStop(1, heart + "00");
      ctx.fillStyle = hg;
      ctx.beginPath();
      ctx.arc(S / 2, S / 2, S * 0.13, 0, Math.PI * 2);
      ctx.fill();
      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    function makeButterflyTexture(wingColor: string, patternColor: string) {
      const S = 128;
      const c = document.createElement("canvas");
      c.width = c.height = S;
      const ctx = c.getContext("2d")!;
      ctx.clearRect(0, 0, S, S);

      ctx.fillStyle = wingColor;
      ctx.beginPath();
      ctx.moveTo(64, 40);
      ctx.bezierCurveTo(15, 5, 5, 55, 60, 75);
      ctx.bezierCurveTo(10, 95, 35, 120, 64, 85);
      ctx.fill();
      ctx.strokeStyle = patternColor;
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.beginPath();
      ctx.moveTo(64, 40);
      ctx.bezierCurveTo(113, 5, 123, 55, 68, 75);
      ctx.bezierCurveTo(118, 95, 93, 120, 64, 85);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.beginPath();
      ctx.arc(35, 45, 5, 0, Math.PI * 2);
      ctx.arc(93, 45, 5, 0, Math.PI * 2);
      ctx.arc(42, 90, 3, 0, Math.PI * 2);
      ctx.arc(86, 90, 3, 0, Math.PI * 2);
      ctx.fill();

      const tex = new THREE.CanvasTexture(c);
      tex.colorSpace = THREE.SRGBColorSpace;
      return tex;
    }

    // --- Noise Utilities ---
    function hash(x: number, y: number) {
      const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453;
      return s - Math.floor(s);
    }
    function sm(t: number) {
      return t * t * (3 - 2 * t);
    }
    function noise(x: number, y: number) {
      const xi = Math.floor(x), yi = Math.floor(y);
      const xf = x - xi, yf = y - yi;
      const a = hash(xi, yi), b = hash(xi + 1, yi), c = hash(xi, yi + 1), d = hash(xi + 1, yi + 1);
      return a + (b - a) * sm(xf) + (c - a) * sm(yf) + (a - b - c + d) * sm(xf) * sm(yf);
    }
    function fbm(x: number, y: number, oct = 4) {
      let v = 0, amp = 1, f = 1, tot = 0;
      for (let i = 0; i < oct; i++) {
        v += amp * noise(x * f, y * f);
        tot += amp;
        amp *= 0.5;
        f *= 2.03;
      }
      return v / tot;
    }

    const groundH = (x: number, z: number) => {
      const d1 = Math.hypot(x - 6, z + 4), d2 = Math.hypot(x + 12, z - 10), d3 = Math.hypot(x + 4, z + 14);
      let h = 5.5 * Math.exp(-(d1 * d1) / 45) + 4.0 * Math.exp(-(d2 * d2) / 70) + 3.0 * Math.exp(-(d3 * d3) / 55);
      h += fbm(x * 0.08, z * 0.08, 5) * 3.2 + fbm(x * 0.4 + 7, z * 0.4, 3) * 0.5;
      const path = Math.sin(x * 0.09) * 6 + Math.sin(x * 0.23) * 2;
      h -= 0.7 * Math.exp(-((z - path) ** 2) / 8);
      return h - 1.5;
    };

    // --- Scene Setup ---
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(49, width / height, 0.1, 800);
    camera.position.set(0, 7.5, 24);

    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      powerPreference: "high-performance",
      precision: "mediump",
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(typeof window !== "undefined" ? window.devicePixelRatio || 1 : 1, 1.5));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;

    container.appendChild(renderer.domElement);

    scene.fog = new THREE.FogExp2(0xd8e8ea, 0.011);

    // --- Procedural Sky Dome ---
    const sky = new THREE.Mesh(
      new THREE.SphereGeometry(400, 32, 15),
      new THREE.ShaderMaterial({
        side: THREE.BackSide,
        depthWrite: false,
        uniforms: {
          top: { value: new THREE.Color(0x3a78c8) },
          mid: { value: new THREE.Color(0x9fd0e8) },
          horizon: { value: new THREE.Color(0xd8e8ea) },
        },
        vertexShader: `varying vec3 vP; void main(){ vP=position; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);} `,
        fragmentShader: `
          uniform vec3 top, mid, horizon; varying vec3 vP;
          void main(){
            float h = normalize(vP).y;
            vec3 c = h > 0.12
              ? mix(mid, top, pow(clamp(h-0.12,0.,1.), 0.65))
              : mix(horizon, mid, clamp((h+0.08)/0.2, 0., 1.));
            gl_FragColor = vec4(c, 1.);
          }`,
      })
    );
    scene.add(sky);

    // --- Soft Painterly Cumulus Clouds ---
    const puffTex = (() => {
      const S = 128;
      const c = document.createElement("canvas");
      c.width = c.height = S;
      const ctx = c.getContext("2d")!;
      const g = ctx.createRadialGradient(64, 64, 6, 64, 64, 60);
      g.addColorStop(0, "rgba(255,255,255,0.92)");
      g.addColorStop(0.5, "rgba(250,252,255,0.6)");
      g.addColorStop(0.85, "rgba(240,246,255,0.2)");
      g.addColorStop(1, "rgba(255,255,255,0)");
      ctx.fillStyle = g;
      ctx.beginPath();
      ctx.arc(64, 64, 60, 0, Math.PI * 2);
      ctx.fill();
      return new THREE.CanvasTexture(c);
    })();

    const cloudGroups: THREE.Group[] = [];
    const CLOUD_COUNT = 8;
    for (let i = 0; i < CLOUD_COUNT; i++) {
      const g = new THREE.Group();
      const puffs = 6 + (Math.random() * 3 | 0);
      const cloudSpan = 12 + Math.random() * 10;

      for (let p = 0; p < puffs; p++) {
        const mat = new THREE.SpriteMaterial({
          map: puffTex,
          transparent: true,
          depthWrite: false,
          fog: true,
          opacity: 0.38 + Math.random() * 0.22,
        });
        const s = new THREE.Sprite(mat);
        const size = 6 + Math.random() * 7;
        s.scale.set(size * 1.35, size * 0.72, 1);
        const px = (p / puffs - 0.5) * cloudSpan + (Math.random() - 0.5) * 3;
        const py = (Math.random() - 0.3) * 2.5;
        const pz = (Math.random() - 0.5) * 4;
        s.position.set(px, py, pz);
        g.add(s);
      }

      const cx = (i / CLOUD_COUNT - 0.5) * 200 + (Math.random() - 0.5) * 25;
      const cy = 20 + Math.random() * 12;
      const cz = -25 - Math.random() * 55;
      g.position.set(cx, cy, cz);
      scene.add(g);
      cloudGroups.push(g);
    }

    // --- Lighting ---
    scene.add(new THREE.HemisphereLight(0xbcd8f0, 0x7a8a50, 0.58));
    const sun = new THREE.DirectionalLight(0xffddb0, 2.0);
    sun.position.set(24, 18, 10);
    sun.castShadow = true;
    sun.shadow.mapSize.set(2048, 2048);
    sun.shadow.camera.left = sun.shadow.camera.bottom = -50;
    sun.shadow.camera.right = sun.shadow.camera.top = 50;
    sun.shadow.camera.far = 120;
    sun.shadow.bias = -0.0004;
    sun.shadow.radius = 3;
    scene.add(sun);

    const fill = new THREE.DirectionalLight(0xc8d8ff, 0.2);
    fill.position.set(-20, 15, -18);
    scene.add(fill);

    // --- Terrain with detailMap shader injection ---
    const groundTex = makeGroundTexture(renderer);
    groundTex.repeat.set(24, 24);
    const groundBump = makeGroundBump(renderer);
    groundBump.repeat.set(24, 24);
    const detailTex = makeGroundTexture(renderer);

    const hillGeo = new THREE.PlaneGeometry(140, 140, 240, 240);
    hillGeo.rotateX(-Math.PI / 2);
    {
      const pos = hillGeo.attributes.position;
      const colors = new Float32Array(pos.count * 3);
      const color = new THREE.Color();
      for (let i = 0; i < pos.count; i++) {
        const x = pos.getX(i), z = pos.getZ(i);
        pos.setY(i, groundH(x, z));
        const macro = fbm(x * 0.02 + 31, z * 0.02, 3);
        const macro2 = fbm(x * 0.008 + 90, z * 0.008, 2);
        color.setHSL(0.24 + (macro2 - 0.5) * 0.05, 0.55, 0.55);
        const b = 0.95 + macro * 0.25 + (macro2 - 0.5) * 0.1;
        colors[i * 3] = color.r * b;
        colors[i * 3 + 1] = color.g * b;
        colors[i * 3 + 2] = color.b * b;
      }
      hillGeo.setAttribute("color", new THREE.BufferAttribute(colors, 3));
      hillGeo.computeVertexNormals();
    }

    const groundMat = new THREE.MeshStandardMaterial({
      map: groundTex,
      bumpMap: groundBump,
      bumpScale: 0.6,
      vertexColors: true,
      roughness: 1.0,
    });

    groundMat.onBeforeCompile = (shader) => {
      shader.uniforms.detailMap = { value: detailTex };
      shader.fragmentShader = `
        uniform sampler2D detailMap;
        varying vec2 vDetailUv;
      ` + shader.fragmentShader.replace(
        "#include <map_fragment>",
        `#include <map_fragment>
         vec4 detailCol = texture2D(detailMap, vDetailUv);
         float dm = dot(detailCol.rgb, vec3(0.299, 0.587, 0.114));
        diffuseColor.rgb *= mix(1.0, dm * 1.7, 0.3);`
      );
      shader.vertexShader = `
        varying vec2 vDetailUv;
      ` + shader.vertexShader.replace(
        "#include <uv_vertex>",
        `#include <uv_vertex>
         vec2 duv = vec2(position.x, -position.z);
         float ca = 0.37, sa = sin(0.37);
         duv = mat2(ca, -sa, sa, ca) * duv;
         vDetailUv = duv * vec2(1.0 / 61.3, 1.0 / 47.7);`
      );
    };

    const hill = new THREE.Mesh(hillGeo, groundMat);
    hill.receiveShadow = true;
    scene.add(hill);

    // --- Real Instanced Grass Blades (180,000 Blades) ---
    function makeBladeGeometry() {
      const SEG = 4, W = 0.016, H = 1.0;
      const pos = [], uv = [], idx = [];
      for (let i = 0; i <= SEG; i++) {
        const t = i / SEG;
        const w = W * (1 - t) * (1 - t * 0.3);
        const bend = t * t * 0.18;
        pos.push(-w, t * H, bend, w, t * H, bend);
        uv.push(0, t, 1, t);
        if (i < SEG) {
          const a = i * 2;
          idx.push(a, a + 1, a + 2, a + 1, a + 3, a + 2);
        }
      }
      const g = new THREE.BufferGeometry();
      g.setAttribute("position", new THREE.Float32BufferAttribute(pos, 3));
      g.setAttribute("uv", new THREE.Float32BufferAttribute(uv, 2));
      g.setIndex(idx);
      g.computeVertexNormals();
      return g;
    }

    const grassUniforms = { uTime: { value: 0 } };
    const grassMat = new THREE.MeshStandardMaterial({
      color: 0xffffff,
      roughness: 1.0,
      side: THREE.DoubleSide,
    });

    grassMat.onBeforeCompile = (shader) => {
      shader.uniforms.uTime = grassUniforms.uTime;
      shader.vertexShader = `
        uniform float uTime;
        attribute float aPhase;
        attribute vec3 aOrigin;
      ` + shader.vertexShader
        .replace("#include <common>", `#include <common>\nvarying float vHeight;\nvarying float vPhase;`)
        .replace("#include <begin_vertex>", `
          vHeight = uv.y;
          vPhase = aPhase;
          vec3 transformed = position;
          float t = uTime * 1.7 + aPhase * 6.2831;
          float sway = sin(t + aOrigin.x * 0.35 + aOrigin.z * 0.5) * 0.5
                     + sin(t * 2.3 + aPhase * 13.0) * 0.2;
          float gust = 0.6 + 0.4 * sin(uTime * 0.5 + aOrigin.x * 0.08 + aOrigin.z * 0.11);
          float bend = sway * gust * uv.y * uv.y * 0.45;
          transformed.x += bend;
          transformed.z += bend * 0.35;
          float d = distance(cameraPosition, aOrigin);
          float fade = 1.0 - smoothstep(28.0, 46.0, d);
          transformed *= fade;
        `);

      shader.fragmentShader = `
        varying float vHeight;
        varying float vPhase;
      ` + shader.fragmentShader.replace("#include <color_fragment>", `
        #include <color_fragment>
        vec3 baseCol = vec3(0.18, 0.30, 0.10);
        vec3 tipCol  = vec3(0.62, 0.78, 0.30);
        diffuseColor.rgb = mix(baseCol, tipCol, pow(vHeight, 0.8));
        diffuseColor.rgb *= 0.85 + 0.3 * fract(vPhase * 7.13);
      `);
    };

    const BLADES = 180000;
    const blades = new THREE.InstancedMesh(makeBladeGeometry(), grassMat, BLADES);
    blades.frustumCulled = false;

    {
      const roots = new Float32Array(BLADES * 3);
      const phases = new Float32Array(BLADES);
      const dummy = new THREE.Object3D();
      let i = 0, guard = 0;
      while (i < BLADES && guard < BLADES * 4) {
        guard++;
        const a = Math.random() * Math.PI * 2;
        const r = Math.sqrt(Math.random()) * 40;
        const x = camera.position.x + Math.cos(a) * r;
        const z = camera.position.z + Math.sin(a) * r;
        if (Math.abs(x) > 66 || Math.abs(z) > 66) continue;
        if (fbm(x * 0.35 + 60, z * 0.35, 3) < 0.28) continue;
        const y = groundH(x, z) - 0.02;
        roots[i * 3] = x;
        roots[i * 3 + 1] = y;
        roots[i * 3 + 2] = z;
        phases[i] = Math.random();

        dummy.position.set(x, y, z);
        dummy.rotation.set((Math.random() - 0.5) * 0.5, Math.random() * Math.PI, (Math.random() - 0.5) * 0.5);
        const h = 0.16 + Math.random() * 0.2;
        dummy.scale.set(0.8 + Math.random() * 0.5, h, 1);
        dummy.updateMatrix();
        blades.setMatrixAt(i, dummy.matrix);
        i++;
      }
      blades.count = i;
      blades.geometry.setAttribute("aOrigin", new THREE.InstancedBufferAttribute(roots, 3));
      blades.geometry.setAttribute("aPhase", new THREE.InstancedBufferAttribute(phases, 1));
    }
    scene.add(blades);

    // --- Flowers ---
    const flowerTexes = [
      makeFlowerTexture("#f7f3e6", "#c9882e"),
      makeFlowerTexture("#e04848", "#7a1f1f"),
      makeFlowerTexture("#eccf45", "#9a7a1a"),
      makeFlowerTexture("#b48ce0", "#4a2a6a"),
    ];
    const headGeo = new THREE.PlaneGeometry(0.34, 0.34);
    const stemMat = new THREE.MeshStandardMaterial({ color: 0x517a38, roughness: 0.9 });
    const flowerGroup = new THREE.Group();
    const heads: THREE.Mesh[] = [];

    for (let cl = 0; cl < 18; cl++) {
      const cx = (Math.random() - 0.5) * 60, cz = (Math.random() - 0.5) * 60;
      const count = 3 + (Math.random() * 4 | 0);
      for (let i = 0; i < count; i++) {
        const x = cx + (Math.random() - 0.5) * 1.4;
        const z = cz + (Math.random() - 0.5) * 1.4;
        const y = groundH(x, z) - 0.02;
        const tex = flowerTexes[(Math.random() * flowerTexes.length) | 0];
        const stemH = 0.18 + Math.random() * 0.22;
        const stem = new THREE.Mesh(new THREE.CylinderGeometry(0.008, 0.012, stemH, 4), stemMat);
        stem.position.set(x, y + stemH / 2, z);
        stem.rotation.z = (Math.random() - 0.5) * 0.4;
        flowerGroup.add(stem);

        const m = new THREE.MeshBasicMaterial({
          map: tex,
          transparent: true,
          depthWrite: false,
          side: THREE.DoubleSide,
        });
        for (let k = 0; k < 2; k++) {
          const head = new THREE.Mesh(headGeo, m);
          head.position.set(x + (k ? 0.01 : -0.01), y + stemH + 0.1, z);
          head.rotation.y = (k * Math.PI) / 2 + Math.random();
          head.rotation.z = (Math.random() - 0.5) * 0.5;
          const s = 0.7 + Math.random() * 0.5;
          head.scale.set(s, s, s);
          flowerGroup.add(head);
          heads.push(head);
        }
      }
    }
    scene.add(flowerGroup);

    // --- Butterflies ---
    const bFlyColors = [
      { wing: "#ff8c1a", pattern: "#2b1704" },
      { wing: "#ffdd33", pattern: "#1f2605" },
      { wing: "#4da6ff", pattern: "#06172b" },
      { wing: "#ff66b2", pattern: "#3a0820" },
    ];
    const bFlyTexes = bFlyColors.map((c) => makeButterflyTexture(c.wing, c.pattern));
    const leftWingGeo = new THREE.PlaneGeometry(0.18, 0.24);
    leftWingGeo.translate(-0.09, 0, 0);
    const rightWingGeo = new THREE.PlaneGeometry(0.18, 0.24);
    rightWingGeo.translate(0.09, 0, 0);

    {
      const uvL = leftWingGeo.attributes.uv;
      for (let i = 0; i < uvL.count; i++) uvL.setX(i, uvL.getX(i) * 0.5);
      const uvR = rightWingGeo.attributes.uv;
      for (let i = 0; i < uvR.count; i++) uvR.setX(i, uvR.getX(i) * 0.5 + 0.5);
    }

    const butterflies: THREE.Group[] = [];
    const bFlyGroup = new THREE.Group();
    const BFLY_COUNT = 16;

    for (let i = 0; i < BFLY_COUNT; i++) {
      const bObj = new THREE.Group();
      const tex = bFlyTexes[i % bFlyTexes.length];
      const mat = new THREE.MeshBasicMaterial({
        map: tex,
        transparent: true,
        side: THREE.DoubleSide,
        depthWrite: false,
      });

      const lWing = new THREE.Mesh(leftWingGeo, mat);
      const rWing = new THREE.Mesh(rightWingGeo, mat);
      bObj.add(lWing);
      bObj.add(rWing);

      const homeX = (Math.random() - 0.5) * 45;
      const homeZ = (Math.random() - 0.5) * 45;
      const speed = 0.5 + Math.random() * 0.7;
      const flapSpeed = 16 + Math.random() * 8;
      const phase = Math.random() * Math.PI * 2;
      const scale = 0.7 + Math.random() * 0.5;
      bObj.scale.set(scale, scale, scale);

      bObj.userData = { homeX, homeZ, speed, flapSpeed, phase, lWing, rWing, lastPos: new THREE.Vector3() };
      bFlyGroup.add(bObj);
      butterflies.push(bObj);
    }
    scene.add(bFlyGroup);

    // --- Animation & Camera Loop ---
    let clock = new THREE.Clock();
    let animId = 0;

    const animate = () => {
      animId = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();
      grassUniforms.uTime.value = t;

      for (const c of cloudGroups) {
        c.position.x += 0.03;
        if (c.position.x > 150) c.position.x = -150;
      }

      for (const h of heads) {
        const p = h.userData.push || 0;
        h.rotation.x = p * 1.2 + Math.sin(t * 1.8 + h.position.x * 3) * 0.06;
        h.rotation.z = p * 0.8;
        if (p > 0.001) h.userData.push = p * 0.92;
      }

      for (const b of butterflies) {
        const u = b.userData;
        const bt = t * u.speed + u.phase;
        const x = u.homeX + Math.sin(bt * 0.7) * 4.5 + Math.cos(bt * 1.3) * 2.0;
        const z = u.homeZ + Math.cos(bt * 0.5) * 4.5 + Math.sin(bt * 1.1) * 2.0;
        const groundY = groundH(x, z);
        const y = groundY + 0.45 + Math.sin(bt * 2.3) * 0.45 + Math.cos(bt * 3.7) * 0.15;

        const currentPos = new THREE.Vector3(x, y, z);
        if (u.lastPos.lengthSq() > 0) {
          const dir = currentPos.clone().sub(u.lastPos);
          if (dir.lengthSq() > 0.00001) {
            b.rotation.y = Math.atan2(dir.x, dir.z);
            b.rotation.x = -dir.y * 1.5;
          }
        }
        u.lastPos.copy(currentPos);
        b.position.copy(currentPos);

        const flap = Math.sin(t * u.flapSpeed + u.phase) * 0.75;
        u.lWing.rotation.y = flap;
        u.rWing.rotation.y = -flap;
      }

      // Smooth camera breathing sway
      camera.position.x = Math.sin(t * 0.12) * 2.0;
      camera.position.y = 7.5 + Math.cos(t * 0.15) * 0.4;
      camera.lookAt(0, 1.2, -8);

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!containerRef.current) return;
      const w = containerRef.current.clientWidth;
      const h = containerRef.current.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener("resize", handleResize);

    sceneRef.current = {
      renderer,
      animId,
      dispose: () => {
        cancelAnimationFrame(animId);
        window.removeEventListener("resize", handleResize);
        if (renderer.domElement && renderer.domElement.parentNode) {
          renderer.domElement.parentNode.removeChild(renderer.domElement);
        }
        renderer.dispose();
      },
    };

    return () => {
      if (sceneRef.current) {
        sceneRef.current.dispose();
      }
    };
  }, []);

  return (
    <div
      className="absolute inset-0 w-full h-full overflow-hidden pointer-events-none z-0"
      style={{ transform: "translateZ(0)", willChange: "transform" }}
    >
      <div ref={containerRef} className="w-full h-full" />
    </div>
  );
};
