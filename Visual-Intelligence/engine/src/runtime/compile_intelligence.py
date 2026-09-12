import os
import re
import json

def parse_frontmatter(text):
    """
    Parses simple key-value YAML frontmatter using regex.
    """
    data = {}
    for line in text.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data

def parse_list_arg(text):
    """
    Parses a string representing a list (e.g. ["a", "b"]) into a Python list.
    """
    cleaned = text.strip().strip('[').strip(']')
    return [item.strip().strip('"').strip("'") for item in cleaned.split(',') if item.strip()]

def compile_domain_rules(domain_path):
    """
    Parses a decision_rules.md file and extracts constraints.
    """
    rules_file = os.path.join(domain_path, "decision_rules.md")
    if not os.path.exists(rules_file):
        print(f"Skipping: {rules_file} does not exist.")
        return []

    with open(rules_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all nested markdown blocks: ```markdown ... ```
    blocks = re.findall(r'```markdown\s*(.*?)\s*```', content, re.DOTALL)
    constraints = []

    for block in blocks:
        # Separate frontmatter and body
        parts = block.split('---')
        if len(parts) < 3:
            continue
        
        frontmatter_text = parts[1]
        body_text = parts[2]
        
        frontmatter = parse_frontmatter(frontmatter_text)
        rule_id = frontmatter.get("id")
        if not rule_id:
            continue

        # Determine level mapping
        level_str = frontmatter.get("level", "Level 3")
        level = 3
        if "Level 1" in level_str:
            level = 1
        elif "Level 2" in level_str:
            level = 2

        # Extract rule description
        desc_match = re.search(r'# Decision Rule:\s*(.*?)\n', body_text)
        description = desc_match.group(1).strip() if desc_match else frontmatter.get("knowledge_unit", "Reasoning Rule")

        # Parse Condition (IF)
        condition = {}
        cond_block_match = re.search(r'## 1\. Condition \(IF\)\s*(.*?)\n##', body_text, re.DOTALL)
        if cond_block_match:
            cond_lines = cond_block_match.group(1).strip().split('\n')
            for line in cond_lines:
                # Matches: Product.FabricType == "Banarasi Silk"
                # Matches: Campaign.Intent == "Luxury Bridal"
                matches = re.findall(r'(?:Product|Campaign)\.(\w+)\s*==\s*(?:"([^"]+)"|\'([^\']+)\'|(\[.*?\]))', line)
                for var, val_str, val_str_alt, val_list in matches:
                    val = val_str or val_str_alt
                    if val:
                        # Append or set
                        if var in condition:
                            if isinstance(condition[var], list):
                                if val not in condition[var]:
                                    condition[var].append(val)
                            else:
                                if condition[var] != val:
                                    condition[var] = [condition[var], val]
                        else:
                            condition[var] = val
                    elif val_list:
                        condition[var] = parse_list_arg(val_list)

        # Parse Action (THEN)
        action = {}
        action_block_match = re.search(r'## 2\. Action \(THEN\)\s*(.*?)\n##', body_text, re.DOTALL)
        if action_block_match:
            action_lines = action_block_match.group(1).strip().split('\n')
            for line in action_lines:
                # 1. PromptCompiler.Inject("...") or PromptCompiler.Inject('...')
                inject_match = re.search(r'PromptCompiler\.Inject\((?:"([^"]+)"|\'([^\']+)\')\)', line)
                if inject_match:
                    val = inject_match.group(1) or inject_match.group(2)
                    action["Prompt_Inject"] = val

                # 2. PromptCompiler.Forbid(["...", "..."])
                forbid_match = re.search(r'PromptCompiler\.Forbid\((.*?)\)', line)
                if forbid_match:
                    action["Prompt_Forbid"] = parse_list_arg(forbid_match.group(1))

                # 3. LightingPlanner.SetPrimarySource / SetKeyAngle / SetLightingProfile
                light_match = re.search(r'LightingPlanner\.Set(?:PrimarySource|KeyAngle|LightingProfile|LightingSetting)\((?:"([^"]+)"|\'([^\']+)\')\)', line)
                if light_match:
                    val = light_match.group(1) or light_match.group(2)
                    action["KeyLight"] = val

                # 4. LightingPlanner.Forbid
                light_forbid_match = re.search(r'LightingPlanner\.Forbid\((.*?)\)', line)
                if light_forbid_match:
                    action["Lighting_Forbid"] = parse_list_arg(light_forbid_match.group(1))

                # 5. CameraPlanner.SetLens / SetFraming
                cam_match = re.search(r'CameraPlanner\.Set(?:Lens|Framing)\((?:"([^"]+)"|\'([^\']+)\'|(\[.*?\]))\)', line)
                if cam_match:
                    val = cam_match.group(1) or cam_match.group(2)
                    if val:
                        action["Lens"] = val
                    elif cam_match.group(3):
                        action["Lens"] = parse_list_arg(cam_match.group(3))

                # 6. PosePlanner.RestrictTo
                pose_restrict_match = re.search(r'PosePlanner\.RestrictTo\((.*?)\)', line)
                if pose_restrict_match:
                    action["Pose_Restrict"] = parse_list_arg(pose_restrict_match.group(1))

        # Infer general category
        category = "Styling"
        if "Lighting" in rule_id or "KeyLight" in action:
            category = "Lighting"
        elif "Camera" in rule_id or "Lens" in action:
            category = "Camera"
        elif "Scene" in rule_id:
            category = "Scene"

        constraints.append({
            "rule_id": rule_id,
            "level": level,
            "category": category,
            "condition": condition,
            "action": action,
            "description": description,
            "weight": float(frontmatter.get("weight", 1.0))
        })

    return constraints

def run_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    # Path: docs/knowledge/Human Expression/ or Intelligence Layer/Human Expression/
    intelligence_dir = os.path.join(base_dir, "docs", "knowledge", "Human Expression")
    if not os.path.exists(intelligence_dir):
        intelligence_dir = os.path.join(base_dir, "Intelligence Layer", "Human Expression")
    if not os.path.exists(intelligence_dir):
        intelligence_dir = r"c:\Users\User\OneDrive\Desktop\Fashion Knowldge Wiki\docs\knowledge\Human Expression"
        
    print(f"Building V2 Compiled Intelligence Database from: {intelligence_dir}")
    all_compiled_rules = []

    if os.path.exists(intelligence_dir):
        for subfolder in os.listdir(intelligence_dir):
            subfolder_path = os.path.join(intelligence_dir, subfolder)
            if os.path.isdir(subfolder_path):
                print(f"Parsing sub-domain: {subfolder}...")
                rules = compile_domain_rules(subfolder_path)
                all_compiled_rules.extend(rules)
                print(f"Loaded {len(rules)} compiled rules from {subfolder}.")

    # Output path: engine/src/runtime/intelligence_compiled.json
    runtime_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(runtime_dir, "intelligence_compiled.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_compiled_rules, f, indent=2)

    print(f"\nSUCCESS: Pipeline compilation complete. Wrote {len(all_compiled_rules)} rules to: {output_path}")

if __name__ == "__main__":
    run_pipeline()
