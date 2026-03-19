# --- Supine postures (on back) ---
SUPINE_POSTURES = [
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "flexion", "weight_bearing_points": ["sacrum", "back_of_head"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "chronic_pain": [
            {"action": "adjust", "condition": "lower_back_pain", "reason": "Pulling knees too hard can strain the lumbar spine.", "recommended_modification": "gentle_hold"},
        ],
        "client_id": "p_knees_to_chest",
        "category": "supine",
        "common_mistakes": ["Holding the breath", "Pulling too aggressively", "Lifting the head and shoulders"],
        "contraindications": [
            {"action": "modify", "condition": "pregnancy", "reason": "Deep compression of the abdomen.", "recommended_modification": "single_knee_to_chest"},
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "straight_up"},
        "modifications": [
            {"instruction": "Hold behind your thighs instead of your shins if knees are sensitive.", "name": "Hold Behind Knees", "target_area": "knees"},
            {"instruction": "Draw one knee at a time toward your chest.", "name": "Single Knee to Chest", "target_area": "lower_back"},
        ],
        "name": {"aliases": ["Apanasana", "Wind-Relieving Pose"], "english": "Knees to Chest", "sanskrit": "Apanasana"},
        "pose_intent": ["Release lower back tension", "Massage the abdominal organs", "Prepare for Bridge or Happy Baby"],
        "progression": {
            "advanced": "Rock gently side to side to massage the spine.",
            "beginner": "Hold behind thighs, gentle pressure.",
            "intermediate": "Clasp hands around shins, draw knees toward armpits.",
        },
        "sensory_cues": [
            {"area": "lower_back", "cue": "Feel your lower back softening into the floor."},
            {"area": "breath", "cue": "Let your exhale help draw your knees closer."},
        ],
        "typical_entries": ["p_bridge", "p_happy_baby", "p_corpse_pose"],
        "typical_exits": ["p_bridge", "p_happy_baby", "p_corpse_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": True, "spinal_shape": "extension", "weight_bearing_points": ["shoulders", "back_of_head", "feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_knees_to_chest", "p_childs_pose"]},
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "lower_back_pain",
                "reason": "Over-clenching the glutes or weak hamstrings can jam the lumbar spine.",
                "recommended_modification": "supported_bridge",
            },
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Feet placed too far or too close to hips places shear force on knees.",
                "recommended_modification": "adjust_foot_distance",
            },
        ],
        "client_id": "p_bridge",
        "category": "supine",
        "common_mistakes": [
            "Turning the head side to side (dangerous for the neck)",
            "Letting the knees splay outward",
            "Over-clenching the glutes instead of using the hamstrings",
        ],
        "contraindications": [
            {
                "action": "caution",
                "condition": "neck_injury",
                "reason": "Bears weight on the cervical spine while in flexion.",
                "recommended_modification": "supported_bridge_low_block",
            }
        ],
        "drishti": {"alternatives": ["heart_center", "closed_eyes"], "primary": "straight_up"},
        "modifications": [
            {
                "instruction": "Slide a yoga block under your sacrum (the hard bone at the base of " "your spine) and rest your weight completely on it.",
                "name": "Supported Bridge",
                "target_area": "lower_back",
            },
            {
                "instruction": "Walk your feet forward or backward until your shins are perfectly " "vertical when your hips are lifted.",
                "name": "Adjust Foot Distance",
                "target_area": "knees",
            },
        ],
        "name": {"aliases": ["Two-Legged Inverted Staff"], "english": "Bridge Pose", "sanskrit": "Setu Bandhasana"},
        "pose_intent": ["Open the chest, heart, and shoulders", "Strengthen the glutes, hamstrings, and erector spinae", "Prepare the spine for deeper backbends or inversions"],
        "progression": {
            "advanced": "Transition into full Wheel Pose (Urdhva Dhanurasana).",
            "beginner": "Dynamic bridge: lifting hips on the inhale, lowering on the exhale.",
            "intermediate": "Hold the lift, interlace hands underneath the back, roll onto the tops of " "the shoulders.",
        },
        "sensory_cues": [
            {"area": "legs", "cue": "Feel your shins pulling slightly backward toward your shoulders to engage your " "hamstrings."},
            {"area": "chest", "cue": "Notice the spaciousness expanding across your collarbones."},
        ],
        "typical_entries": ["p_corpse_pose", "p_knees_to_chest"],
        "typical_exits": ["p_corpse_pose", "p_happy_baby", "p_knees_to_chest"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "mild_flexion", "weight_bearing_points": ["entire_back", "sacrum", "back_of_head"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_corpse_pose", "p_bridge"]},
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Pulling down on the feet can torque the knee if hips are tight.",
                "recommended_modification": "hold_behind_knees",
            },
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "If the tailbone lifts completely off the floor, it strains the lumbar " "spine.",
                "recommended_modification": "tailbone_down",
            },
        ],
        "client_id": "p_happy_baby",
        "category": "supine",
        "common_mistakes": [
            "Lifting the tailbone and lower back off the floor",
            "Lifting the head and shoulders up to reach the feet",
            "Feet dropping down toward the glutes instead of pointing at the ceiling",
        ],
        "contraindications": [
            {
                "action": "modify_or_avoid",
                "condition": "pregnancy",
                "reason": "Lying flat on the back in later stages compresses the vena cava.",
                "recommended_modification": "seated_bound_angle",
            }
        ],
        "drishti": {"alternatives": ["straight_up"], "primary": "closed_eyes"},
        "modifications": [
            {
                "instruction": "Instead of grabbing your feet, wrap your hands behind your thighs to " "safely pull your knees wide.",
                "name": "Hold Behind Knees",
                "target_area": "knees",
            },
            {
                "instruction": "Focus on pressing your tailbone flat into the mat, even if it means " "you can't pull your knees as low.",
                "name": "Tailbone Down",
                "target_area": "lower_back",
            },
        ],
        "name": {"aliases": ["Dead Bug Pose"], "english": "Happy Baby Pose", "sanskrit": "Ananda Balasana"},
        "pose_intent": ["Gently stretch the inner groins and back spine", "Release the lower back and sacrum", "Calm the mind and relieve stress"],
        "progression": {
            "advanced": "Gently rock side to side, massaging the spine against the floor.",
            "beginner": "Hold the backs of the thighs, tailbone rooted.",
            "intermediate": "Hold the outer edges of the feet, ankles stacked directly over knees.",
        },
        "sensory_cues": [
            {"area": "lower_back", "cue": "Let your tailbone grow heavy, anchoring you to the earth."},
            {"area": "hips", "cue": "Feel the gentle, broad opening across your inner thighs."},
        ],
        "typical_entries": ["p_knees_to_chest", "p_bridge"],
        "typical_exits": ["p_corpse_pose", "p_knees_to_chest"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["back_of_head", "shoulders", "sacrum", "calves", "heels"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "lower_back_pain",
                "reason": "Lying flat can cause the lumbar spine to arch due to tight hip flexors " "(psoas pull).",
                "recommended_modification": "bolster_under_knees",
            }
        ],
        "client_id": "p_corpse_pose",
        "category": "supine",
        "common_mistakes": ["Fidgeting or adjusting clothing", "Keeping the teeth clenched or the tongue pressed against the roof of the mouth", "Skipping the pose entirely"],
        "contraindications": [
            {
                "action": "modify",
                "condition": "pregnancy",
                "reason": "Lying flat in late stages restricts blood flow in the inferior vena " "cava.",
                "recommended_modification": "side_lying_savasana",
            }
        ],
        "drishti": {"alternatives": ["inward_focus"], "primary": "closed_eyes"},
        "modifications": [
            {
                "instruction": "Place a rolled blanket or bolster beneath your knees to allow your " "lower back to flatten and release.",
                "name": "Bolster Under Knees",
                "target_area": "lower_back",
            },
            {"instruction": "Lie on your left side with a pillow between your knees for comfort.", "name": "Side-Lying Savasana", "target_area": "cardiovascular"},
        ],
        "name": {"aliases": ["Final Relaxation"], "english": "Corpse Pose", "sanskrit": "Savasana"},
        "pose_intent": [
            "Integrate the physical and energetic benefits of the practice",
            "Lower the heart rate and blood pressure",
            "Transition into a state of deep meditation and rest",
        ],
        "progression": {
            "advanced": "Achieve complete stillness of body and mind for 10+ minutes without falling " "asleep.",
            "beginner": "Use props for physical comfort.",
            "intermediate": "Lie flat, focusing on sequential muscle relaxation.",
        },
        "sensory_cues": [
            {"area": "full_body", "cue": "Feel your body becoming so heavy it begins to sink into the floor."},
            {"area": "breath", "cue": "Let your breath become natural, soft, and completely effortless."},
            {"area": "face", "cue": "Notice the space between your eyebrows softening and widening."},
        ],
        "typical_entries": ["p_happy_baby", "p_halasana", "p_fish_pose", "p_knees_to_chest"],
        "typical_exits": ["p_easy_pose", "p_knees_to_chest"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "extension", "weight_bearing_points": ["crown_of_head", "buttocks", "forearms"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_corpse_pose"]},
        "chronic_pain": [
            {"action": "modify", "condition": "neck_pain", "reason": "Weight on the crown can strain the cervical spine.", "recommended_modification": "supported_fish"},
        ],
        "client_id": "p_fish_pose",
        "category": "supine",
        "common_mistakes": ["Dumping weight into the head", "Over-arching the lower back", "Holding the breath"],
        "contraindications": [
            {"action": "avoid", "condition": "neck_injury", "reason": "Weight-bearing on the cervical spine.", "recommended_modification": "bridge_pose"},
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "straight_up"},
        "modifications": [
            {"instruction": "Place a folded blanket under your upper back to reduce neck pressure.", "name": "Supported Fish", "target_area": "neck"},
            {"instruction": "Keep your legs in Butterfly or extended with minimal arch.", "name": "Gentle Fish", "target_area": "spine"},
        ],
        "name": {"aliases": ["Matsyasana"], "english": "Fish Pose", "sanskrit": "Matsyasana"},
        "pose_intent": ["Open the chest and throat", "Counterpose for Shoulder Stand", "Stretch the front of the neck"],
        "progression": {
            "advanced": "Full expression with legs in Lotus, arms overhead.",
            "beginner": "Supported with a block under the upper back.",
            "intermediate": "Legs extended, crown of head lightly on the floor.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Feel your heart lifting toward the ceiling."},
            {"area": "throat", "cue": "Notice the gentle stretch along the front of your neck."},
        ],
        "typical_entries": ["p_shoulder_stand"],
        "typical_exits": ["p_corpse_pose"],
    },
]
