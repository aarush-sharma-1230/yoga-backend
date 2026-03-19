# --- Seated postures (sit bones) ---
SEATED_POSTURES = [
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["sit_bones", "outer_ankles"], "laterality": {"type": "symmetrical", "active_side": "neutral"}},
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Deep flexion and external rotation strain the medial knee ligaments.",
                "recommended_modification": "blocks_under_knees",
            },
            {"action": "adjust", "condition": "hip_tightness", "reason": "Tight hips cause the lower back to round backward.", "recommended_modification": "sit_on_cushion"},
        ],
        "client_id": "p_easy_pose",
        "category": "seated",
        "common_mistakes": ["Slumping the lower back", "Jutting the chin forward (tech neck)", "Forcing the knees toward the floor"],
        "contraindications": [{"action": "caution", "condition": "sciatica", "reason": "Sitting flat can compress the sciatic nerve.", "recommended_modification": "sit_on_block"}],
        "drishti": {"alternatives": ["third_eye"], "primary": "closed_eyes"},
        "modifications": [
            {"instruction": "Sit on the edge of a folded blanket or block to elevate your hips " "above your knees.", "name": "Elevated Seat", "target_area": "hips"},
            {"instruction": "Place blocks or pillows under your knees so they can rest without " "hanging in the air.", "name": "Blocks Under Knees", "target_area": "knees"},
        ],
        "name": {"aliases": ["Cross-legged Seat"], "english": "Easy Pose", "sanskrit": "Sukhasana"},
        "pose_intent": ["Promote groundedness and mental clarity", "Open the hips and stretch the knees and ankles", "Provide a steady seat for meditation and pranayama"],
        "progression": {
            "advanced": "Hold for extended meditation without fidgeting or losing spinal integrity.",
            "beginner": "Sit on a bolster, legs loosely crossed.",
            "intermediate": "Sit flat on the floor, shins crossed, maintaining a long spine.",
        },
        "sensory_cues": [
            {"area": "pelvis", "cue": "Feel your sit bones heavy and rooted into the prop beneath you."},
            {"area": "shoulders", "cue": "Let your shoulders melt down away from your ears."},
        ],
        "typical_entries": ["p_staff_pose"],
        "typical_exits": ["p_seated_forward_fold", "p_table_top", "p_staff_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["sit_bones", "heels", "palms (lightly)"], "laterality": {"type": "symmetrical", "active_side": "neutral"}},
        "chronic_pain": [
            {"action": "adjust", "condition": "tight_hamstrings", "reason": "Pulls the pelvis backward, rounding the lower spine.", "recommended_modification": "sit_on_blanket"},
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Requires significant core strength to sit upright; weakness causes lumbar " "strain.",
                "recommended_modification": "wall_support",
            },
        ],
        "client_id": "p_staff_pose",
        "category": "seated",
        "common_mistakes": ["Leaning backward on the hands", "Rounding the upper back", "Letting the feet splay open"],
        "contraindications": [
            {
                "action": "caution",
                "condition": "sciatica",
                "reason": "90-degree hip flexion with straight legs stretches the sciatic nerve " "aggressively.",
                "recommended_modification": "bend_knees",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "toes"},
        "modifications": [
            {"instruction": "Sit on a folded blanket to tilt your pelvis forward and relieve the " "hamstrings.", "name": "Sit on Blanket", "target_area": "hamstrings"},
            {"instruction": "Sit with your back pressed flat against a wall to help support your " "spine.", "name": "Wall Support", "target_area": "lower_back"},
        ],
        "name": {"aliases": ["Seated Staff"], "english": "Staff Pose", "sanskrit": "Dandasana"},
        "pose_intent": ["Improve postural awareness", "Strengthen back muscles and core", "Stretch the hamstrings and calves"],
        "progression": {
            "advanced": "Perfect 90-degree angle, hands hovering off the floor, fully supported by the " "core.",
            "beginner": "Sit on a blanket, knees slightly bent.",
            "intermediate": "Sit flat, legs straight, heels pressing away.",
        },
        "sensory_cues": [
            {"area": "full_body", "cue": "Imagine your torso and legs forming a perfect right angle."},
            {"area": "spine", "cue": "Feel the crown of your head reaching up as your tailbone roots down."},
        ],
        "typical_entries": ["p_downward_dog", "p_easy_pose"],
        "typical_exits": ["p_seated_forward_fold", "p_head_to_knee_left", "p_head_to_knee_right", "p_easy_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "flexion", "weight_bearing_points": ["sit_bones", "heels", "calves"], "laterality": {"type": "symmetrical", "active_side": "neutral"}},
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Causes extreme pulling on the lower back if legs remain straight.",
                "recommended_modification": "use_strap",
            }
        ],
        "client_id": "p_seated_forward_fold",
        "category": "seated",
        "common_mistakes": ["Rounding the upper back to force the head down", "Pulling aggressively with the arms", "Locking the knees"],
        "contraindications": [
            {"action": "avoid", "condition": "herniated_disc", "reason": "Intense seated spinal flexion forces disc material backward.", "recommended_modification": "staff_pose"},
            {"action": "modify", "condition": "pregnancy", "reason": "Compresses the abdomen.", "recommended_modification": "wide_leg_forward_fold"},
        ],
        "drishti": {"alternatives": ["shins", "closed_eyes"], "primary": "toes"},
        "modifications": [
            {"instruction": "Loop a strap around your feet and hold the ends to keep your spine " "long as you gently pull.", "name": "Use a Strap", "target_area": "hamstrings"},
            {"instruction": "Keep a generous bend in your knees, prioritizing a straight back over " "straight legs.", "name": "Microbend Knees", "target_area": "lower_back"},
        ],
        "name": {"aliases": ["Seated Forward Fold"], "english": "Seated Forward Bend", "sanskrit": "Paschimottanasana"},
        "pose_intent": ["Deeply stretch the entire posterior chain (hamstrings, calves, spine)", "Calm the nervous system", "Stimulate abdominal organs"],
        "progression": {
            "advanced": "Forehead resting comfortably on the shins, elbows resting on the floor.",
            "beginner": "Use a strap, knees bent, spine straight.",
            "intermediate": "Hold the outer edges of the feet, chest reaching toward the toes.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Think about pulling your heart toward your toes rather than your nose to your " "knees."},
            {"area": "hamstrings", "cue": "Feel a deep, calming release traveling up the back of your legs."},
        ],
        "typical_entries": ["p_staff_pose"],
        "typical_exits": ["p_staff_pose", "p_head_to_knee_left", "p_head_to_knee_right"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "flexion_with_mild_rotation",
            "weight_bearing_points": ["sit_bones", "extended_leg_heel", "bent_knee_outer_edge"],
            "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_head_to_knee_right"},
        },
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "knee_pain",
                "reason": "Deep flexion and external rotation of the bent knee stresses the medial " "meniscus.",
                "recommended_modification": "block_under_bent_knee",
            },
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Pulls the pelvis into posterior tilt, rounding the lower back excessively.",
                "recommended_modification": "use_strap",
            },
        ],
        "client_id": "p_head_to_knee_left",
        "category": "seated",
        "common_mistakes": [
            "Rounding the upper back to force the head down",
            "Letting the extended leg roll outward",
            "Collapsing the chest over the bent knee instead of the straight leg",
        ],
        "contraindications": [
            {
                "action": "avoid",
                "condition": "herniated_disc",
                "reason": "The combination of spinal flexion and mild rotation is highly " "stressful on lumbar discs.",
                "recommended_modification": "staff_pose",
            }
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "toes"},
        "modifications": [
            {
                "instruction": "Place a block or folded blanket beneath your bent knee so it has " "solid support and doesn't hang in the air.",
                "name": "Block Under Bent Knee",
                "target_area": "knees",
            },
            {"instruction": "Loop a strap around the foot of your extended leg to keep your spine " "long as you fold.", "name": "Use a Strap", "target_area": "hamstrings"},
        ],
        "name": {"aliases": ["Seated Head to Knee Left"], "english": "Head-to-Knee Forward Bend (Left Leg Bent)", "sanskrit": "Janu Sirsasana"},
        "pose_intent": ["Stretch the hamstrings, spine, and groins", "Calm the brain and help relieve mild depression", "Stimulate the liver and kidneys"],
        "progression": {
            "advanced": "Rest forehead on the shin, clasp wrists beyond the extended foot.",
            "beginner": "Sit on a folded blanket, use a strap, keep spine completely straight.",
            "intermediate": "Hold the foot, bending elbows out to the sides, lowering the chest toward " "the thigh.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Imagine aiming your heart toward your toes, keeping the front of your body " "long."},
            {"area": "lower_back", "cue": "Feel a gentle, twisting release in your lower back on the side of the bent " "knee."},
        ],
        "typical_entries": ["p_staff_pose", "p_seated_forward_fold"],
        "typical_exits": ["p_seated_forward_fold", "p_easy_pose", "p_staff_pose"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "flexion_with_mild_rotation",
            "weight_bearing_points": ["sit_bones", "extended_leg_heel", "bent_knee_outer_edge"],
            "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_head_to_knee_left"},
        },
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "knee_pain",
                "reason": "Deep flexion and external rotation of the bent knee stresses the medial " "meniscus.",
                "recommended_modification": "block_under_bent_knee",
            },
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Pulls the pelvis into posterior tilt, rounding the lower back excessively.",
                "recommended_modification": "use_strap",
            },
        ],
        "client_id": "p_head_to_knee_right",
        "category": "seated",
        "common_mistakes": [
            "Rounding the upper back to force the head down",
            "Letting the extended leg roll outward",
            "Collapsing the chest over the bent knee instead of the straight leg",
        ],
        "contraindications": [
            {
                "action": "avoid",
                "condition": "herniated_disc",
                "reason": "The combination of spinal flexion and mild rotation is highly " "stressful on lumbar discs.",
                "recommended_modification": "staff_pose",
            }
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "toes"},
        "modifications": [
            {
                "instruction": "Place a block or folded blanket beneath your bent knee so it has " "solid support and doesn't hang in the air.",
                "name": "Block Under Bent Knee",
                "target_area": "knees",
            },
            {"instruction": "Loop a strap around the foot of your extended leg to keep your spine " "long as you fold.", "name": "Use a Strap", "target_area": "hamstrings"},
        ],
        "name": {"aliases": ["Seated Head to Knee Right"], "english": "Head-to-Knee Forward Bend (Right Leg Bent)", "sanskrit": "Janu Sirsasana"},
        "pose_intent": ["Stretch the hamstrings, spine, and groins", "Calm the brain and help relieve mild depression", "Stimulate the liver and kidneys"],
        "progression": {
            "advanced": "Rest forehead on the shin, clasp wrists beyond the extended foot.",
            "beginner": "Sit on a folded blanket, use a strap, keep spine completely straight.",
            "intermediate": "Hold the foot, bending elbows out to the sides, lowering the chest toward " "the thigh.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Imagine aiming your heart toward your toes, keeping the front of your body " "long."},
            {"area": "lower_back", "cue": "Feel a gentle, twisting release in your lower back on the side of the bent " "knee."},
        ],
        "typical_entries": ["p_staff_pose", "p_seated_forward_fold"],
        "typical_exits": ["p_seated_forward_fold", "p_easy_pose", "p_staff_pose"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "neutral_to_mild_extension",
            "weight_bearing_points": ["front_shin", "back_knee", "top_of_back_foot", "forearms_if_folded"],
            "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_pigeon_right"},
        },
        "chronic_pain": [
            {
                "action": "avoid",
                "condition": "knee_pain",
                "reason": "Intense lateral torque is placed on the front knee if the hip lacks " "mobility.",
                "recommended_modification": "supine_figure_four",
            },
            {
                "action": "modify",
                "condition": "hip_tightness",
                "reason": "Causes the practitioner to roll completely onto one side, misaligning the " "spine.",
                "recommended_modification": "prop_under_hip",
            },
        ],
        "client_id": "p_pigeon_left",
        "category": "seated",
        "common_mistakes": [
            "Rolling onto the outer hip of the bent leg",
            "Forcing the front shin parallel to the mat, causing knee torque",
            "Tensing the shoulders while folding forward",
        ],
        "contraindications": [
            {
                "action": "avoid",
                "condition": "recent_surgery",
                "reason": "Hip replacements or recent knee surgeries cannot tolerate extreme " "external rotation.",
                "recommended_modification": "supine_figure_four",
            }
        ],
        "drishti": {"alternatives": ["floor_straight_down"], "primary": "closed_eyes"},
        "modifications": [
            {
                "instruction": "Lie on your back, cross your right ankle over your left thigh, and " "pull your left knee toward your chest. This protects the knee " "completely.",
                "name": "Supine Figure Four",
                "target_area": "knees",
            },
            {
                "instruction": "Place a blanket or block under the hip of your bent leg to keep your " "pelvis level with the floor.",
                "name": "Prop Under Hip",
                "target_area": "hips",
            },
        ],
        "name": {"aliases": ["Half Pigeon Left", "Sleeping Pigeon"], "english": "Pigeon Pose (Left Leg Forward)", "sanskrit": "Eka Pada Rajakapotasana"},
        "pose_intent": [
            "Deeply stretch the hip rotators (gluteus, piriformis) of the front leg",
            "Stretch the hip flexors (psoas) of the back leg",
            "Release emotional and physical tension stored in the pelvis",
        ],
        "progression": {
            "advanced": "Rest forehead on the floor, arms extended forward, front shin parallel to the " "top of the mat.",
            "beginner": "Keep the front heel close to the groin, stay lifted on the hands.",
            "intermediate": "Walk hands forward and lower down to the forearms.",
        },
        "sensory_cues": [
            {"area": "hips", "cue": "Send your breath directly into the tightness of your outer hip."},
            {"area": "full_body", "cue": "With every exhale, imagine sinking a millimeter deeper into the mat."},
        ],
        "typical_entries": ["p_downward_dog", "p_table_top"],
        "typical_exits": ["p_downward_dog", "p_table_top"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "neutral_to_mild_extension",
            "weight_bearing_points": ["front_shin", "back_knee", "top_of_back_foot", "forearms_if_folded"],
            "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_pigeon_left"},
        },
        "chronic_pain": [
            {
                "action": "avoid",
                "condition": "knee_pain",
                "reason": "Intense lateral torque is placed on the front knee if the hip lacks " "mobility.",
                "recommended_modification": "supine_figure_four",
            },
            {
                "action": "modify",
                "condition": "hip_tightness",
                "reason": "Causes the practitioner to roll completely onto one side, misaligning the " "spine.",
                "recommended_modification": "prop_under_hip",
            },
        ],
        "client_id": "p_pigeon_right",
        "category": "seated",
        "common_mistakes": [
            "Rolling onto the outer hip of the bent leg",
            "Forcing the front shin parallel to the mat, causing knee torque",
            "Tensing the shoulders while folding forward",
        ],
        "contraindications": [
            {
                "action": "avoid",
                "condition": "recent_surgery",
                "reason": "Hip replacements or recent knee surgeries cannot tolerate extreme " "external rotation.",
                "recommended_modification": "supine_figure_four",
            }
        ],
        "drishti": {"alternatives": ["floor_straight_down"], "primary": "closed_eyes"},
        "modifications": [
            {
                "instruction": "Lie on your back, cross your left ankle over your right thigh, and " "pull your right knee toward your chest. This protects the knee " "completely.",
                "name": "Supine Figure Four",
                "target_area": "knees",
            },
            {
                "instruction": "Place a blanket or block under the hip of your bent leg to keep your " "pelvis level with the floor.",
                "name": "Prop Under Hip",
                "target_area": "hips",
            },
        ],
        "name": {"aliases": ["Half Pigeon Right", "Sleeping Pigeon"], "english": "Pigeon Pose (Right Leg Forward)", "sanskrit": "Eka Pada Rajakapotasana"},
        "pose_intent": [
            "Deeply stretch the hip rotators (gluteus, piriformis) of the front leg",
            "Stretch the hip flexors (psoas) of the back leg",
            "Release emotional and physical tension stored in the pelvis",
        ],
        "progression": {
            "advanced": "Rest forehead on the floor, arms extended forward, front shin parallel to the " "top of the mat.",
            "beginner": "Keep the front heel close to the groin, stay lifted on the hands.",
            "intermediate": "Walk hands forward and lower down to the forearms.",
        },
        "sensory_cues": [
            {"area": "hips", "cue": "Send your breath directly into the tightness of your outer hip."},
            {"area": "full_body", "cue": "With every exhale, imagine sinking a millimeter deeper into the mat."},
        ],
        "typical_entries": ["p_downward_dog", "p_table_top"],
        "typical_exits": ["p_downward_dog", "p_table_top"],
    },
]
