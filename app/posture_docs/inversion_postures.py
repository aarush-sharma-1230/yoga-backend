# --- Inversion postures (head below heart) ---
INVERSION_POSTURES = [
    {
        "anatomical_signature": {"is_inverted": True, "spinal_shape": "neutral", "weight_bearing_points": ["palms", "feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 1,
            "muscular_load": {"core": 2, "upper_body": 4, "lower_body": 1},
            "mobility_load": {"posterior_chain": 4, "hips_and_pelvis": 2, "spine": 1, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "wrist_pain", "reason": "Weight-bearing compresses the wrist joint.", "recommended_modification": "dolphin_pose"},
            {"action": "adjust", "condition": "tight_hamstrings", "reason": "Limited flexibility strains the back.", "recommended_modification": "bend_knees"},
        ],
        "client_id": "p_downward_dog",
        "category": "inversion",
        "common_mistakes": ["Rounding the back", "Dumping weight into the wrists", "Forcing heels to the floor"],
        "contraindications": [
            {"action": "modify_or_avoid", "condition": "hypertension", "reason": "Inversion may increase blood pressure.", "recommended_modification": "puppy_pose"},
            {"action": "avoid", "condition": "glaucoma", "reason": "Increases intraocular pressure.", "recommended_modification": None},
            {"action": "modify", "condition": "vertigo", "reason": "Change in head position causes dizziness.", "recommended_modification": "puppy_pose"},
        ],
        "drishti": {"alternatives": ["between_feet"], "primary": "navel"},
        "modifications": [
            {"instruction": "Lower your forearms to the mat, pressing firmly through the forearms " "to lift hips.", "name": "Dolphin Pose", "target_area": "wrists"},
            {
                "instruction": "Bring your knees to the mat, walk hands forward, and lower your " "chest, keeping head above heart.",
                "name": "Puppy Pose",
                "target_area": "cardiovascular",
            },
            {"instruction": "Bend your knees deeply while keeping your spine long and hips lifting " "up.", "name": "Bend Knees", "target_area": "hamstrings"},
        ],
        "name": {"aliases": ["Down Dog", "Inverted V"], "english": "Downward Facing Dog", "sanskrit": "Adho Mukha Svanasana"},
        "pose_intent": ["Lengthen the spine", "Stretch the posterior chain (hamstrings, calves)", "Strengthen shoulders and arms"],
        "progression": {
            "advanced": "Fully extend the legs with stable shoulders and grounded heels.",
            "beginner": "Keep knees bent and focus on lengthening the spine.",
            "intermediate": "Work toward straightening the legs while maintaining spinal length.",
        },
        "sensory_cues": [
            {"area": "spine", "cue": "Feel the length growing from your hands to your hips."},
            {"area": "legs", "cue": "Imagine your heels gently melting toward the mat."},
        ],
        "typical_entries": ["p_plank", "p_table_top", "p_cow", "p_chaturanga", "p_upward_dog"],
        "typical_exits": ["p_plank", "p_forward_fold", "p_childs_pose", "p_table_top", "p_chaturanga", "p_warrior_1_left", "p_warrior_1_right", "p_pigeon_left", "p_pigeon_right"],
    },
    {
        "anatomical_signature": {"is_inverted": True, "spinal_shape": "flexion", "weight_bearing_points": ["shoulders", "back_of_head", "elbows"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_fish_pose"]},
        "intensity_profile": {
            "overall_exertion": 5,
            "balance_requirement": 2,
            "muscular_load": {"core": 4, "upper_body": 2, "lower_body": 1},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 1, "spine": 5, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {"action": "avoid", "condition": "neck_pain", "reason": "Flattening the cervical curve under load can herniate discs.", "recommended_modification": "legs_up_the_wall"}
        ],
        "client_id": "p_shoulder_stand",
        "category": "inversion",
        "common_mistakes": [
            "Turning the head while in the pose (can cause severe injury)",
            "Splaying the elbows too wide, losing structural support",
            "Dumping weight into the neck instead of pressing through the shoulders",
        ],
        "contraindications": [
            {"action": "avoid", "condition": "glaucoma", "reason": "Massive increase in intraocular pressure.", "recommended_modification": None},
            {
                "action": "avoid",
                "condition": "hypertension",
                "reason": "Forces a large volume of blood toward the heart and brain under " "compression.",
                "recommended_modification": "legs_up_the_wall",
            },
            {"action": "avoid", "condition": "neck_injury", "reason": "Extreme cervical flexion bearing body weight.", "recommended_modification": "legs_up_the_wall"},
            {"action": "modify_or_avoid", "condition": "pregnancy", "reason": "Risk of falling and abdominal compression.", "recommended_modification": "legs_up_the_wall"},
        ],
        "drishti": {"alternatives": ["chest"], "primary": "toes"},
        "modifications": [
            {
                "instruction": "Scoot your hips against a wall and extend your legs straight up it, " "keeping your back perfectly flat on the floor.",
                "name": "Legs Up The Wall",
                "target_area": "neck",
            },
            {
                "instruction": "Place neatly folded blankets under your shoulders so your head rests " "on the floor, preserving the natural curve of your neck.",
                "name": "Blanket Support",
                "target_area": "neck",
            },
        ],
        "name": {"aliases": ["Shoulderstand", "Queen of Poses"], "english": "Supported Shoulder Stand", "sanskrit": "Salamba Sarvangasana"},
        "pose_intent": ["Improve venous blood return from the legs", "Stimulate the thyroid and parathyroid glands", "Calm the central nervous system deeply"],
        "progression": {
            "advanced": "Perfectly vertical alignment from shoulders to toes, hands resting near the " "shoulder blades.",
            "beginner": "Legs Up The Wall or a block under the sacrum with legs in the air.",
            "intermediate": "Use blanket support, hands supporting the mid-back, legs angled slightly " "back.",
        },
        "sensory_cues": [
            {"area": "neck", "cue": "Keep your gaze locked strictly upward—protecting your neck is paramount."},
            {"area": "legs", "cue": "Imagine the blood flowing out of your feet, cascading gently down your legs to " "cool your heart."},
        ],
        "typical_entries": ["p_bridge", "p_halasana"],
        "typical_exits": ["p_halasana", "p_corpse_pose", "p_fish_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": True, "spinal_shape": "flexion", "weight_bearing_points": ["shoulders", "back_of_head", "toes"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_fish_pose", "p_corpse_pose"]},
        "intensity_profile": {
            "overall_exertion": 5,
            "balance_requirement": 2,
            "muscular_load": {"core": 4, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 5, "hips_and_pelvis": 2, "spine": 5, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {"action": "caution", "condition": "lower_back_pain", "reason": "Deep spinal flexion can aggravate lumbar discs.", "recommended_modification": "supported_bridge"}
        ],
        "client_id": "p_halasana",
        "category": "inversion",
        "common_mistakes": [
            "Turning the head from side to side",
            "Forcing the feet to the floor, compromising the neck",
            "Collapsing the chest into the chin, restricting the airway",
        ],
        "contraindications": [
            {"action": "avoid", "condition": "glaucoma", "reason": "Severe increase in intraocular pressure.", "recommended_modification": None},
            {"action": "avoid", "condition": "hypertension", "reason": "Blood flow forced toward the head under compression.", "recommended_modification": "legs_up_the_wall"},
            {"action": "avoid", "condition": "neck_injury", "reason": "Extreme cervical flexion under load.", "recommended_modification": "seated_forward_fold"},
        ],
        "drishti": {"alternatives": ["straight_up", "closed_eyes"], "primary": "navel"},
        "modifications": [
            {
                "instruction": "If your feet don't reach the floor easily, rest your toes on a chair " "or bolster placed behind your head.",
                "name": "Feet on Chair",
                "target_area": "hamstrings",
            },
            {"instruction": "Skip the neck compression entirely and simply rest your legs up a " "wall.", "name": "Legs Up The Wall", "target_area": "neck"},
        ],
        "name": {"aliases": ["Plough Pose"], "english": "Plow Pose", "sanskrit": "Halasana"},
        "pose_intent": ["Deeply stretch the cervical and thoracic spine", "Stimulate the abdominal organs and thyroid", "Prepare the body for final relaxation"],
        "progression": {
            "advanced": "Toes tucked on the floor behind the head, arms interlaced and pressing into " "the mat.",
            "beginner": "Avoid full pose. Practice Legs Up The Wall.",
            "intermediate": "Support the lower back with hands, toes resting on a prop.",
        },
        "sensory_cues": [
            {"area": "neck", "cue": "Keep your gaze straight up; imagine a hollow space between your neck and the " "floor."},
            {"area": "spine", "cue": "Feel the deep, quiet stretch traveling down the entire length of your spine."},
        ],
        "typical_entries": ["p_shoulder_stand", "p_bridge"],
        "typical_exits": ["p_corpse_pose", "p_happy_baby", "p_shoulder_stand"],
    },
]
