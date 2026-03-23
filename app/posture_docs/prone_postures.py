# --- Prone postures (belly/body toward floor) ---
PRONE_POSTURES = [
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["palms", "knees", "shins"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 1,
            "balance_requirement": 1,
            "muscular_load": {"core": 2, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "wrist_pain", "reason": "Weight-bearing compresses the wrists.", "recommended_modification": "fists_or_forearms"},
            {"action": "modify", "condition": "knee_pain", "reason": "Direct pressure on the knees.", "recommended_modification": "padded_knees"},
        ],
        "client_id": "p_table_top",
        "category": "prone",
        "common_mistakes": ["Rounding the spine", "Shrugging the shoulders", "Holding the breath"],
        "contraindications": [],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "floor_slightly_forward"},
        "modifications": [
            {"instruction": "Place a folded blanket under your knees for cushioning.", "name": "Padded Knees", "target_area": "knees"},
            {"instruction": "Make fists or use forearms if wrists are sensitive.", "name": "Fists or Forearms", "target_area": "wrists"},
        ],
        "name": {"aliases": ["All Fours", "Hands and Knees"], "english": "Table Top Pose", "sanskrit": "Bharmanasana"},
        "pose_intent": ["Establish neutral spine on all fours", "Prepare for Cat-Cow and transitions", "Build wrist and core awareness"],
        "progression": {
            "advanced": "Maintain perfect neutrality while moving through transitions.",
            "beginner": "Focus on stacking shoulders over wrists, hips over knees.",
            "intermediate": "Engage the core to support the spine.",
        },
        "sensory_cues": [
            {"area": "spine", "cue": "Imagine your spine as a flat table from crown to tailbone."},
            {"area": "hands", "cue": "Spread your fingers wide and press evenly through the palms."},
        ],
        "typical_entries": ["p_childs_pose", "p_easy_pose", "p_downward_dog"],
        "typical_exits": ["p_cat", "p_cow", "p_childs_pose", "p_downward_dog", "p_plank", "p_pigeon_left", "p_pigeon_right"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "flexion", "weight_bearing_points": ["palms", "knees", "shins"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_cow"]},
        "intensity_profile": {
            "overall_exertion": 1,
            "balance_requirement": 1,
            "muscular_load": {"core": 2, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 3, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "wrist_pain", "reason": "Weight-bearing in full extension compresses the wrists.", "recommended_modification": "fists_or_forearms"},
            {"action": "modify", "condition": "knee_pain", "reason": "Direct pressure on the patella against the floor.", "recommended_modification": "padded_knees"},
        ],
        "client_id": "p_cat",
        "category": "prone",
        "common_mistakes": ["Forcing the chin too hard into the chest", "Shrugging the shoulders up toward the ears", "Locking the elbows"],
        "contraindications": [
            {
                "action": "modify",
                "condition": "neck_injury",
                "reason": "Dropping the head completely can strain injured cervical discs.",
                "recommended_modification": "neutral_neck_cat",
            }
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "navel"},
        "modifications": [
            {"instruction": "Keep your gaze between your hands rather than tucking your chin to " "your chest.", "name": "Neutral Neck Cat", "target_area": "neck"},
            {"instruction": "Make fists with your hands or drop to your forearms to relieve wrist " "compression.", "name": "Fists or Forearms", "target_area": "wrists"},
            {"instruction": "Place a folded blanket directly under your knees for cushioning.", "name": "Padded Knees", "target_area": "knees"},
        ],
        "name": {"aliases": ["Cat Stretch"], "english": "Cat Pose", "sanskrit": "Marjaryasana"},
        "pose_intent": ["Stretch the posterior torso and neck", "Provide a gentle massage to the spine and belly organs", "Release tension in the cervical and thoracic spine"],
        "progression": {
            "advanced": "Engage the pelvic floor (Mula Bandha) deeply at the peak of the flexion.",
            "beginner": "Focus on moving the middle back toward the ceiling.",
            "intermediate": "Coordinate the movement perfectly with the exhale.",
        },
        "sensory_cues": [
            {"area": "spine", "cue": "Imagine a string pulling the center of your back up toward the ceiling."},
            {"area": "upper_back", "cue": "Feel your shoulder blades spreading wide apart."},
        ],
        "typical_entries": ["p_table_top", "p_cow"],
        "typical_exits": ["p_cow", "p_childs_pose", "p_downward_dog"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "extension", "weight_bearing_points": ["palms", "knees", "shins"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_cat"]},
        "intensity_profile": {
            "overall_exertion": 1,
            "balance_requirement": 1,
            "muscular_load": {"core": 2, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 3, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Dumping weight into the lower back causes painful facet joint compression.",
                "recommended_modification": "engage_core",
            },
            {"action": "modify", "condition": "wrist_pain", "reason": "Weight-bearing in extension compresses wrists.", "recommended_modification": "fists_or_forearms"},
        ],
        "client_id": "p_cow",
        "category": "prone",
        "common_mistakes": ["Collapsing heavily into the lower back without core support", "Cranking the neck upward", "Bending the elbows"],
        "contraindications": [
            {"action": "modify", "condition": "neck_injury", "reason": "Looking up sharply compresses the cervical vertebrae.", "recommended_modification": "look_forward"}
        ],
        "drishti": {"alternatives": ["straight_ahead", "tip_of_nose"], "primary": "third_eye"},
        "modifications": [
            {"instruction": "Keep your gaze straight ahead rather than craning your neck to look " "up.", "name": "Look Forward", "target_area": "neck"},
            {"instruction": "Keep a slight lifting action in your belly to support your lower back " "as it arches.", "name": "Engage Core", "target_area": "lower_back"},
        ],
        "name": {"aliases": ["Cow Stretch"], "english": "Cow Pose", "sanskrit": "Bitilasana"},
        "pose_intent": ["Stretch the front torso and neck", "Open the chest to encourage deeper breathing", "Mobilize the lumbar and cervical spine"],
        "progression": {
            "advanced": "Isolate the movement, allowing the spine to ripple sequentially from tailbone " "to crown.",
            "beginner": "Focus on dropping the belly gently without forcing.",
            "intermediate": "Broaden the collarbones and pull the heart forward through the arms.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Feel your collarbones widening like a smile."},
            {"area": "chest", "cue": "Imagine your heart melting forward between your biceps."},
        ],
        "typical_entries": ["p_table_top", "p_cat"],
        "typical_exits": ["p_cat", "p_downward_dog", "p_childs_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "flexion", "weight_bearing_points": ["shins", "forehead", "forearms"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 1,
            "balance_requirement": 1,
            "muscular_load": {"core": 1, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 2, "shoulders_and_chest": 1},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "knee_pain", "reason": "Deep flexion compresses the meniscus.", "recommended_modification": "blanket_under_knees_or_hips"},
            {
                "action": "modify",
                "condition": "ankle_stiffness",
                "reason": "Deep plantar flexion stretches the anterior ankle tightly.",
                "recommended_modification": "rolled_blanket_under_ankles",
            },
        ],
        "client_id": "p_childs_pose",
        "category": "prone",
        "common_mistakes": ["Forcing hips to heels causing knee pain", "Holding tension in the shoulders"],
        "contraindications": [{"action": "modify", "condition": "pregnancy", "reason": "Compression of the abdomen.", "recommended_modification": "wide_knee_childs_pose"}],
        "drishti": {"alternatives": ["inward"], "primary": "closed_eyes"},
        "modifications": [
            {"instruction": "Take your knees as wide as the mat to create space for your belly and " "chest.", "name": "Wide Knee Childs Pose", "target_area": "hips"},
            {"instruction": "Place a rolled blanket between your calves and hamstrings to reduce " "knee flexion.", "name": "Blanket Support", "target_area": "knees"},
        ],
        "name": {"aliases": ["Resting Pose"], "english": "Child's Pose", "sanskrit": "Balasana"},
        "pose_intent": ["Release tension in the lower back", "Gently stretch hips and thighs", "Calm the mind and regulate breath"],
        "progression": {
            "advanced": "Knees together, arms back, breath directed fully into the posterior ribcage.",
            "beginner": "Use a bolster under the torso for full support.",
            "intermediate": "Knees wide, arms actively reaching forward.",
        },
        "sensory_cues": [
            {"area": "hips", "cue": "Feel your hips sinking heavier toward your heels with every exhale."},
            {"area": "head", "cue": "Notice the solid support of the earth beneath your forehead."},
        ],
        "typical_entries": ["p_table_top", "p_downward_dog"],
        "typical_exits": ["p_table_top", "p_downward_dog", "p_cobra"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["palms", "toes"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 1,
            "muscular_load": {"core": 4, "upper_body": 4, "lower_body": 2},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "wrist_pain",
                "reason": "Full body weight is loaded onto wrists in 90-degree extension.",
                "recommended_modification": "forearm_plank",
            },
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "If the core weakens, the lower back arches and takes the load.",
                "recommended_modification": "knees_down_plank",
            },
        ],
        "client_id": "p_plank",
        "category": "prone",
        "common_mistakes": ["Dropping the hips and sagging the lower back", "Piking the hips up too high", "Collapsing between the shoulder blades"],
        "contraindications": [
            {
                "action": "caution",
                "condition": "hypertension",
                "reason": "Intense isometric holds can cause temporary blood pressure spikes if " "breath is held.",
                "recommended_modification": "knees_down_plank",
            }
        ],
        "drishti": {"alternatives": ["slightly_forward"], "primary": "top_of_mat"},
        "modifications": [
            {"instruction": "Lower down to your forearms, keeping your elbows directly beneath " "your shoulders.", "name": "Forearm Plank", "target_area": "wrists"},
            {
                "instruction": "Gently drop your knees to the mat, maintaining a straight line from " "your head to your knees.",
                "name": "Knees Down Plank",
                "target_area": "lower_back",
            },
        ],
        "name": {"aliases": ["High Plank", "Upper Push-up"], "english": "Plank Pose", "sanskrit": "Phalakasana"},
        "pose_intent": ["Build core, shoulder, and arm strength", "Create full-body isometric tension", "Prepare for arm balances and transitions"],
        "progression": {
            "advanced": "Shift weight slightly forward onto the tiptoes in preparation for Chaturanga.",
            "beginner": "Knees on the mat, focusing on pressing the floor away.",
            "intermediate": "Full high plank, heels pressing back, core braced.",
        },
        "sensory_cues": [
            {"area": "core", "cue": "Feel your belly button pulling up toward your spine."},
            {"area": "upper_back", "cue": "Imagine pushing the floor away to fill the space between your shoulder " "blades."},
        ],
        "typical_entries": ["p_downward_dog", "p_forward_fold", "p_table_top"],
        "typical_exits": ["p_chaturanga", "p_downward_dog", "p_childs_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["palms", "tops_of_feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 5,
            "balance_requirement": 1,
            "muscular_load": {"core": 4, "upper_body": 5, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 1, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "wrist_pain", "reason": "Full body weight on wrists in extension.", "recommended_modification": "forearm_chaturanga"},
            {"action": "adjust", "condition": "lower_back_pain", "reason": "Weak core causes lumbar sag.", "recommended_modification": "knees_down_chaturanga"},
        ],
        "client_id": "p_chaturanga",
        "category": "prone",
        "common_mistakes": ["Dropping the hips", "Splaying the elbows out", "Shrugging the shoulders"],
        "contraindications": [
            {"action": "modify", "condition": "shoulder_injury", "reason": "Heavy load on the shoulder girdle.", "recommended_modification": "knees_down_chaturanga"},
        ],
        "drishti": {"alternatives": ["slightly_forward"], "primary": "floor_slightly_forward"},
        "modifications": [
            {"instruction": "Lower to your forearms instead of palms.", "name": "Forearm Chaturanga", "target_area": "wrists"},
            {"instruction": "Lower your knees to the mat, maintaining a straight line from head to knees.", "name": "Knees Down Chaturanga", "target_area": "core"},
        ],
        "name": {"aliases": ["Four-Limbed Staff", "Low Plank"], "english": "Chaturanga Dandasana", "sanskrit": "Chaturanga Dandasana"},
        "pose_intent": ["Strengthen arms, shoulders, and core", "Build the foundation for vinyasa flow", "Prepare for Cobra or Upward Dog"],
        "progression": {
            "advanced": "Full expression with elbows at 90 degrees, body in one straight line.",
            "beginner": "Knees down, focus on elbow alignment.",
            "intermediate": "Lower with control from Plank, hover briefly before transitioning.",
        },
        "sensory_cues": [
            {"area": "core", "cue": "Draw your belly button up toward your spine."},
            {"area": "arms", "cue": "Keep your elbows hugging your ribs as you lower."},
        ],
        "typical_entries": ["p_plank", "p_halfway_lift", "p_downward_dog"],
        "typical_exits": ["p_cobra", "p_upward_dog", "p_downward_dog"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "extension", "weight_bearing_points": ["pelvis", "tops_of_feet", "palms (lightly)"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 1,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 1},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 2, "spine": 4, "shoulders_and_chest": 4},
        },
        "chronic_pain": [
            {"action": "adjust", "condition": "lower_back_pain", "reason": "Pushing up too high jams the lumbar facet joints.", "recommended_modification": "baby_cobra"}
        ],
        "client_id": "p_cobra",
        "category": "prone",
        "common_mistakes": [
            "Using arm strength to push up instead of back strength",
            "Crunching the back of the neck by looking too far up",
            "Letting the elbows splay out to the sides",
        ],
        "contraindications": [
            {"action": "avoid", "condition": "pregnancy", "reason": "Direct pressure on the abdomen is unsafe.", "recommended_modification": "cow_pose"},
            {
                "action": "modify_or_avoid",
                "condition": "herniated_disc",
                "reason": "Spinal extension can compress affected posterior discs.",
                "recommended_modification": "sphinx_pose",
            },
        ],
        "drishti": {"alternatives": ["tip_of_nose"], "primary": "straight_ahead"},
        "modifications": [
            {
                "instruction": "Lift only your chest off the mat using your back muscles, keeping " "little to no weight in your hands.",
                "name": "Baby Cobra",
                "target_area": "lower_back",
            },
            {"instruction": "Slide your forearms forward and rest on your elbows to reduce the " "arch in your back.", "name": "Sphinx Pose", "target_area": "lower_back"},
        ],
        "name": {"aliases": ["Baby Cobra"], "english": "Cobra Pose", "sanskrit": "Bhujangasana"},
        "pose_intent": ["Strengthen the spinal erectors", "Open the chest and shoulders", "Counteract forward-hunching posture"],
        "progression": {
            "advanced": "Full expression with elbows slightly bent, chest pulling actively forward.",
            "beginner": "Baby cobra, hands hovering off the mat.",
            "intermediate": "Palms lightly pressing, lifting higher while keeping the pubis grounded.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Feel the front of your chest peeling away from the earth."},
            {"area": "shoulders", "cue": "Imagine your shoulder blades sliding down toward your back pockets."},
        ],
        "typical_entries": ["p_chaturanga"],
        "typical_exits": ["p_downward_dog", "p_childs_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "mild_extension", "weight_bearing_points": ["forearms", "pelvis", "tops_of_feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": True, "recommended_counter_poses": ["p_childs_pose"]},
        "intensity_profile": {
            "overall_exertion": 2,
            "balance_requirement": 1,
            "muscular_load": {"core": 2, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 3, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "If glutes and core relax completely, the lower back takes all the " "compression.",
                "recommended_modification": "slide_elbows_forward",
            }
        ],
        "client_id": "p_sphinx",
        "category": "prone",
        "common_mistakes": ["Sinking the chest between the shoulders", "Clenching the glutes too tightly", "Looking too far upward"],
        "contraindications": [{"action": "avoid", "condition": "pregnancy", "reason": "Direct pressure on the abdomen is unsafe.", "recommended_modification": "cow_pose"}],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "straight_ahead"},
        "modifications": [
            {
                "instruction": "Walk your elbows slightly ahead of your shoulders to decrease the " "intensity of the backbend.",
                "name": "Slide Elbows Forward",
                "target_area": "lower_back",
            }
        ],
        "name": {"aliases": ["Supported Cobra"], "english": "Sphinx Pose", "sanskrit": "Salamba Bhujangasana"},
        "pose_intent": ["Provide a gentle, supported backbend", "Open the chest and lungs safely", "Alleviate lower back fatigue"],
        "progression": {
            "advanced": "Transition into Seal Pose by straightening the arms.",
            "beginner": "Elbows slightly forward, focusing on deep breathing.",
            "intermediate": "Elbows directly under shoulders, actively dragging forearms back to pull " "chest forward.",
        },
        "sensory_cues": [
            {"area": "spine", "cue": "Feel the gentle traction as you energetically pull your elbows toward your " "hips."},
            {"area": "chest", "cue": "Notice the quiet, steady opening across your collarbones."},
        ],
        "typical_entries": ["p_cobra"],
        "typical_exits": ["p_childs_pose"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "extension", "weight_bearing_points": ["palms", "tops_of_feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 1,
            "muscular_load": {"core": 3, "upper_body": 4, "lower_body": 2},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 5, "shoulders_and_chest": 5},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "lower_back_pain", "reason": "Hanging in the joints causes severe lower back compression.", "recommended_modification": "cobra_pose"},
            {"action": "modify", "condition": "wrist_pain", "reason": "Bears significant body weight in deep wrist extension.", "recommended_modification": "sphinx_pose"},
        ],
        "client_id": "p_upward_dog",
        "category": "prone",
        "common_mistakes": [
            "Letting the thighs rest on the floor (which turns it into a poorly aligned Cobra)",
            "Hanging the head back completely, crunching the neck",
            "Shoulders creeping up to the ears",
        ],
        "contraindications": [
            {"action": "avoid", "condition": "pregnancy", "reason": "Overstretches the abdomen and compresses the lumbar spine.", "recommended_modification": "cow_pose"},
            {"action": "avoid", "condition": "herniated_disc", "reason": "Intense spinal extension can severely aggravate disc issues.", "recommended_modification": "sphinx_pose"},
        ],
        "drishti": {"alternatives": ["slightly_upward"], "primary": "tip_of_nose"},
        "modifications": [
            {"instruction": "Keep your thighs and pelvis on the floor and maintain a slight bend " "in your elbows.", "name": "Cobra Pose", "target_area": "lower_back"}
        ],
        "name": {"aliases": ["Up Dog"], "english": "Upward Facing Dog", "sanskrit": "Urdhva Mukha Svanasana"},
        "pose_intent": ["Deeply stretch the anterior chain (chest, abdomen, hip flexors)", "Strengthen the wrists, arms, and spine", "Stimulate abdominal organs"],
        "progression": {
            "advanced": "Full extension with thighs lifted, chest pulling fiercely through the upper " "arms.",
            "beginner": "Substitute with Cobra Pose.",
            "intermediate": "Lift thighs off the mat, pressing firmly through the tops of the feet.",
        },
        "sensory_cues": [
            {"area": "chest", "cue": "Imagine your heart shining brightly forward like a headlight."},
            {"area": "legs", "cue": "Feel the tops of your feet pressing down so firmly that your kneecaps lift."},
        ],
        "typical_entries": ["p_chaturanga"],
        "typical_exits": ["p_downward_dog", "p_childs_pose"],
    },
]
