# --- Supine postures (on back) ---
SUPINE_POSTURES = [
    {
        "anatomical_signature": {"is_inverted": True, "spinal_shape": "extension", "weight_bearing_points": ["shoulders", "back_of_head", "feet"]},
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
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "mild_flexion", "weight_bearing_points": ["entire_back", "sacrum", "back_of_head"]},
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
        "typical_exits": ["p_corpse_pose", "p_knees_to_chest", "p_supine_twist"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["back_of_head", "shoulders", "sacrum", "calves", "heels"]},
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "lower_back_pain",
                "reason": "Lying flat can cause the lumbar spine to arch due to tight hip flexors " "(psoas pull).",
                "recommended_modification": "bolster_under_knees",
            }
        ],
        "client_id": "p_corpse_pose",
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
        "typical_entries": ["p_happy_baby", "p_supine_twist", "p_halasana"],
        "typical_exits": ["p_easy_pose", "session_end"],
    },
]
