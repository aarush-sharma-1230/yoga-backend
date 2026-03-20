# --- Standing postures (weight on feet) ---
STANDING_POSTURES = [
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 1,
            "balance_requirement": 1,
            "muscular_load": {"core": 1, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 1, "shoulders_and_chest": 1},
        },
        "chronic_pain": [
            {"action": "adjust", "condition": "lower_back_pain", "reason": "Anterior pelvic tilt creates lumbar compression.", "recommended_modification": "tuck_tailbone"},
            {"action": "adjust", "condition": "knee_pain", "reason": "Locking the knees causes joint strain.", "recommended_modification": "microbend_knees"},
        ],
        "client_id": "p_mountain",
        "category": "standing",
        "common_mistakes": ["Locking the knees", "Dumping weight entirely into the heels", "Arching the lower back excessively"],
        "contraindications": [
            {"action": "caution", "condition": "vertigo", "reason": "Closing eyes while standing can cause loss of balance.", "recommended_modification": "eyes_open"}
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "straight_ahead"},
        "modifications": [
            {"instruction": "Keep your gaze softly focused on a point in front of you.", "name": "Eyes Open", "target_area": "full_body"},
            {"instruction": "Keep a tiny softness in the back of your knees to engage the " "quadriceps.", "name": "Microbend Knees", "target_area": "knees"},
        ],
        "name": {"aliases": ["Samasthiti", "Standing Pose"], "english": "Mountain Pose", "sanskrit": "Tadasana"},
        "pose_intent": ["Establish grounding and physical equilibrium", "Improve posture and spinal alignment", "Calm the nervous system"],
        "progression": {
            "advanced": "Close eyes and maintain equilibrium relying on internal proprioception.",
            "beginner": "Stand with feet hip-width apart for better balance.",
            "intermediate": "Bring big toes to touch, heels slightly apart.",
        },
        "sensory_cues": [
            {"area": "feet", "cue": "Feel the four corners of your feet rooting deeply into the earth."},
            {"area": "spine", "cue": "Imagine a string pulling the crown of your head directly up."},
        ],
        "typical_entries": ["p_forward_fold", "p_chair"],
        "typical_exits": ["p_upward_salute", "p_chair", "p_forward_fold", "p_tree_left", "p_tree_right"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "mild_extension", "weight_bearing_points": ["feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 1,
            "balance_requirement": 1,
            "muscular_load": {"core": 1, "upper_body": 2, "lower_body": 1},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 1, "spine": 1, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {"action": "modify", "condition": "shoulder_pain", "reason": "Shoulder flexion can pinch the subacromial space.", "recommended_modification": "cactus_arms"},
            {"action": "adjust", "condition": "neck_pain", "reason": "Looking up at the thumbs strains the cervical spine.", "recommended_modification": "neutral_neck"},
        ],
        "client_id": "p_upward_salute",
        "category": "standing",
        "common_mistakes": ["Shrugging shoulders up to the ears", "Flaring the lower ribs outward", "Craning the neck back excessively"],
        "contraindications": [
            {
                "action": "modify",
                "condition": "hypertension",
                "reason": "Raising arms overhead can temporarily elevate blood pressure.",
                "recommended_modification": "hands_at_heart",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "thumbs"},
        "modifications": [
            {"instruction": "Bend your elbows to 90 degrees instead of reaching straight up.", "name": "Cactus Arms", "target_area": "shoulders"},
            {"instruction": "Keep your gaze straight forward rather than looking up at your hands.", "name": "Neutral Neck", "target_area": "neck"},
        ],
        "name": {"aliases": ["Raised Hands Pose"], "english": "Upward Salute", "sanskrit": "Urdhva Hastasana"},
        "pose_intent": ["Lengthen the lateral sides of the body", "Open the chest and shoulders", "Stimulate the respiratory system"],
        "progression": {
            "advanced": "Add a slight upper backbend while keeping the core braced.",
            "beginner": "Keep arms shoulder-width apart.",
            "intermediate": "Bring palms to touch overhead.",
        },
        "sensory_cues": [
            {"area": "torso", "cue": "Notice the lift from your ribcage as you reach upward."},
            {"area": "ribs", "cue": "Feel the space opening up along your side body."},
        ],
        "typical_entries": ["p_mountain"],
        "typical_exits": ["p_forward_fold", "p_chair", "p_mountain"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 1,
            "muscular_load": {"core": 3, "upper_body": 2, "lower_body": 4},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 2, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Deep flexion combined with weight-bearing strains the patellar tendon.",
                "recommended_modification": "shallow_bend",
            },
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Weak core causes the lumbar spine to arch heavily (anterior tilt).",
                "recommended_modification": "tuck_tailbone",
            },
        ],
        "client_id": "p_chair",
        "category": "standing",
        "common_mistakes": ["Knees tracking past the toes", "Arching the lower back (duck butt)", "Dropping the chest toward the thighs"],
        "contraindications": [
            {
                "action": "modify",
                "condition": "hypertension",
                "reason": "Arms overhead combined with large muscle engagement increases cardiac " "load.",
                "recommended_modification": "hands_at_heart",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "slightly_upward"},
        "modifications": [
            {"instruction": "Bend your knees only a few inches, keeping the weight entirely in " "your heels.", "name": "Shallow Bend", "target_area": "knees"},
            {
                "instruction": "Bring your hands to prayer position at your chest to reduce shoulder " "and cardiovascular strain.",
                "name": "Hands at Heart",
                "target_area": "shoulders",
            },
        ],
        "name": {"aliases": ["Fierce Pose", "Lightning Bolt Pose"], "english": "Chair Pose", "sanskrit": "Utkatasana"},
        "pose_intent": ["Strengthen thighs, calves, and ankles", "Engage the core and erector spinae", "Build internal heat"],
        "progression": {
            "advanced": "Hold the deep bend while lifting the heels off the floor.",
            "beginner": "Feet hip-width apart, shallow bend.",
            "intermediate": "Big toes touching, thighs parallel to the floor.",
        },
        "sensory_cues": [{"area": "feet", "cue": "Feel the weight shifting back into your heels."}, {"area": "thighs", "cue": "Notice the heat building in your quadriceps."}],
        "typical_entries": ["p_mountain", "p_upward_salute"],
        "typical_exits": ["p_forward_fold", "p_mountain", "p_halfway_lift"],
    },
    {
        "anatomical_signature": {"is_inverted": True, "spinal_shape": "flexion", "weight_bearing_points": ["feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 2,
            "balance_requirement": 1,
            "muscular_load": {"core": 1, "upper_body": 1, "lower_body": 2},
            "mobility_load": {"posterior_chain": 4, "hips_and_pelvis": 2, "spine": 2, "shoulders_and_chest": 1},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Straight legs force the stretch into the lower back instead of the " "hamstrings.",
                "recommended_modification": "knees_deeply_bent",
            }
        ],
        "client_id": "p_forward_fold",
        "category": "standing",
        "common_mistakes": ["Locking the knees", "Hinging from the lower back instead of the hips", "Holding tension in the neck"],
        "contraindications": [
            {"action": "avoid", "condition": "glaucoma", "reason": "Head below the heart increases intraocular pressure.", "recommended_modification": "halfway_lift"},
            {
                "action": "modify_or_avoid",
                "condition": "hypertension",
                "reason": "Inversion can cause a sudden rush of blood to the head.",
                "recommended_modification": "halfway_lift",
            },
            {
                "action": "modify",
                "condition": "herniated_disc",
                "reason": "Spinal flexion under the load of the torso can aggravate discs.",
                "recommended_modification": "knees_deeply_bent",
            },
        ],
        "drishti": {"alternatives": ["navel", "closed_eyes"], "primary": "tip_of_nose"},
        "modifications": [
            {"instruction": "Bend your knees as much as needed to let your ribs rest on your " "thighs.", "name": "Knees Deeply Bent", "target_area": "hamstrings"},
            {"instruction": "Place your hands on yoga blocks to bring the floor closer to you.", "name": "Blocks Under Hands", "target_area": "lower_back"},
        ],
        "name": {"aliases": ["Standing Forward Bend"], "english": "Standing Forward Fold", "sanskrit": "Uttanasana"},
        "pose_intent": ["Stretch hamstrings and calves", "Release tension in the cervical and lumbar spine", "Calm the nervous system (mild inversion)"],
        "progression": {
            "advanced": "Palms flat on the floor beside feet, chest against thighs.",
            "beginner": "Deep bend in the knees, hands on shins or blocks.",
            "intermediate": "Legs straighter, fingertips touching the floor.",
        },
        "sensory_cues": [
            {"area": "neck", "cue": "Let your head hang heavy like a ripe fruit."},
            {"area": "hamstrings", "cue": "Feel the stretch wrapping around the back of your legs."},
        ],
        "typical_entries": ["p_mountain", "p_upward_salute", "p_halfway_lift", "p_chair"],
        "typical_exits": ["p_halfway_lift", "p_plank", "p_mountain"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "symmetrical", "active_side": "neutral"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 2,
            "balance_requirement": 1,
            "muscular_load": {"core": 3, "upper_body": 1, "lower_body": 1},
            "mobility_load": {"posterior_chain": 3, "hips_and_pelvis": 1, "spine": 2, "shoulders_and_chest": 1},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Lifting the torso requires core strength; weakness drops the load into the " "lower back.",
                "recommended_modification": "hands_on_thighs",
            }
        ],
        "client_id": "p_halfway_lift",
        "category": "standing",
        "common_mistakes": ["Rounding the upper back", "Looking too far forward, straining the neck", "Locking the knees"],
        "contraindications": [
            {"action": "caution", "condition": "neck_injury", "reason": "Looking up can hyperextend the cervical spine.", "recommended_modification": "look_down"}
        ],
        "drishti": {"alternatives": ["tip_of_nose"], "primary": "floor_slightly_forward"},
        "modifications": [
            {"instruction": "Place your hands on your thighs instead of your shins for extra " "spinal support.", "name": "Hands on Thighs", "target_area": "lower_back"},
            {"instruction": "Keep your gaze straight down at the floor to maintain a neutral neck.", "name": "Look Down", "target_area": "neck"},
        ],
        "name": {"aliases": ["Standing Half Forward Bend"], "english": "Halfway Lift", "sanskrit": "Ardha Uttanasana"},
        "pose_intent": ["Lengthen the spine", "Prepare the back for movement", "Stretch the hamstrings safely"],
        "progression": {
            "advanced": "Fingertips on the floor in line with the toes, spine perfectly flat.",
            "beginner": "Hands on thighs, slight bend in knees.",
            "intermediate": "Hands on shins, legs straight.",
        },
        "sensory_cues": [
            {"area": "spine", "cue": "Imagine making your back as flat as a table."},
            {"area": "spine", "cue": "Feel the crown of your head pulling forward away from your tailbone."},
        ],
        "typical_entries": ["p_forward_fold", "p_downward_dog"],
        "typical_exits": ["p_forward_fold", "p_plank", "p_chaturanga"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "mild_extension", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_warrior_1_right"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 2, "lower_body": 4},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 4, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {"action": "adjust", "condition": "knee_pain", "reason": "Deep lunge places lateral and sheer stress on the front knee.", "recommended_modification": "shorten_stance"},
            {
                "action": "modify",
                "condition": "ankle_stiffness",
                "reason": "The back foot requires strong dorsiflexion and rotation.",
                "recommended_modification": "high_lunge_heel_up",
            },
        ],
        "client_id": "p_warrior_1_left",
        "category": "standing",
        "common_mistakes": ["Front knee collapsing inward", "Over-arching the lower back", "Back foot lifting off the floor"],
        "contraindications": [
            {
                "action": "modify",
                "condition": "hypertension",
                "reason": "Arms overhead combined with large muscle engagement increases cardiac " "load.",
                "recommended_modification": "hands_at_heart",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "thumbs"},
        "modifications": [
            {"instruction": "Step your back foot slightly closer to the front and decrease the " "bend in your front knee.", "name": "Shorten Stance", "target_area": "knees"},
            {"instruction": "Lift your back heel off the floor so all toes point forward, " "relieving ankle pressure.", "name": "High Lunge (Heel Up)", "target_area": "ankles"},
        ],
        "name": {"aliases": ["Warrior I Left"], "english": "Warrior 1 (Left Leg Forward)", "sanskrit": "Virabhadrasana I"},
        "pose_intent": ["Strengthen quadriceps, glutes, and ankles", "Stretch the hip flexors of the back leg", "Open the chest and shoulders"],
        "progression": {
            "advanced": "Palms touching overhead, gaze up, back leg perfectly straight.",
            "beginner": "Short stance, hands on hips.",
            "intermediate": "Deepen the front knee bend to 90 degrees, arms overhead.",
        },
        "sensory_cues": [{"area": "feet", "cue": "Feel your back heel anchoring you down."}, {"area": "hips", "cue": "Notice the stretch across the front of your back hip."}],
        "typical_entries": ["p_downward_dog", "p_mountain"],
        "typical_exits": ["p_warrior_2_left", "p_plank", "p_mountain"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "mild_extension", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_warrior_1_left"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 2, "lower_body": 4},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 4, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {"action": "adjust", "condition": "knee_pain", "reason": "Deep lunge places lateral and sheer stress on the front knee.", "recommended_modification": "shorten_stance"},
            {
                "action": "modify",
                "condition": "ankle_stiffness",
                "reason": "The back foot requires strong dorsiflexion and rotation.",
                "recommended_modification": "high_lunge_heel_up",
            },
        ],
        "client_id": "p_warrior_1_right",
        "category": "standing",
        "common_mistakes": ["Front knee collapsing inward", "Over-arching the lower back", "Back foot lifting off the floor"],
        "contraindications": [
            {
                "action": "modify",
                "condition": "hypertension",
                "reason": "Arms overhead combined with large muscle engagement increases cardiac " "load.",
                "recommended_modification": "hands_at_heart",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "thumbs"},
        "modifications": [
            {"instruction": "Step your back foot slightly closer to the front and decrease the " "bend in your front knee.", "name": "Shorten Stance", "target_area": "knees"},
            {"instruction": "Lift your back heel off the floor so all toes point forward, " "relieving ankle pressure.", "name": "High Lunge (Heel Up)", "target_area": "ankles"},
        ],
        "name": {"aliases": ["Warrior I Right"], "english": "Warrior 1 (Right Leg Forward)", "sanskrit": "Virabhadrasana I"},
        "pose_intent": ["Strengthen quadriceps, glutes, and ankles", "Stretch the hip flexors of the back leg", "Open the chest and shoulders"],
        "progression": {
            "advanced": "Palms touching overhead, gaze up, back leg perfectly straight.",
            "beginner": "Short stance, hands on hips.",
            "intermediate": "Deepen the front knee bend to 90 degrees, arms overhead.",
        },
        "sensory_cues": [{"area": "feet", "cue": "Feel your back heel anchoring you down."}, {"area": "hips", "cue": "Notice the stretch across the front of your back hip."}],
        "typical_entries": ["p_downward_dog", "p_mountain"],
        "typical_exits": ["p_warrior_2_right", "p_plank", "p_mountain"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_warrior_2_right"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 3, "lower_body": 4},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "shoulder_pain",
                "reason": "Holding arms parallel to the floor fatigues the deltoids and traps.",
                "recommended_modification": "hands_on_hips",
            },
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Front knee flexion combined with external hip rotation can strain the " "medial collateral ligament (MCL).",
                "recommended_modification": "shorten_stance",
            },
        ],
        "client_id": "p_warrior_2_left",
        "category": "standing",
        "common_mistakes": ["Leaning the torso over the front leg", "Front knee collapsing inward past the big toe", "Shrugging the shoulders"],
        "contraindications": [
            {
                "action": "caution",
                "condition": "vertigo",
                "reason": "Turning the head sharply over the front hand can trigger dizziness.",
                "recommended_modification": "neutral_neck",
            }
        ],
        "drishti": {"alternatives": ["side_wall"], "primary": "front_middle_finger"},
        "modifications": [
            {"instruction": "Rest your hands on your hips to release tension in the shoulders and " "neck.", "name": "Hands on Hips", "target_area": "shoulders"},
            {"instruction": "Keep your chest and gaze facing the side of the room rather than " "turning your head.", "name": "Neutral Neck", "target_area": "neck"},
        ],
        "name": {"aliases": ["Warrior II Left"], "english": "Warrior 2 (Left Leg Forward)", "sanskrit": "Virabhadrasana II"},
        "pose_intent": ["Open the hips and groin", "Strengthen the legs and ankles", "Build stamina and concentration"],
        "progression": {
            "advanced": "Deepest expression with perfect external rotation of the front hip.",
            "beginner": "Shorter stance, shallow bend in the front knee.",
            "intermediate": "Front thigh parallel to the floor, arms actively reaching apart.",
        },
        "sensory_cues": [
            {"area": "arms", "cue": "Imagine your arms are being gently pulled in opposite directions."},
            {"area": "legs", "cue": "Feel the power and stability in your legs."},
        ],
        "typical_entries": ["p_warrior_1_left", "p_downward_dog", "p_mountain"],
        "typical_exits": ["p_triangle_left", "p_plank"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_warrior_2_left"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 3, "lower_body": 4},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "shoulder_pain",
                "reason": "Holding arms parallel to the floor fatigues the deltoids and traps.",
                "recommended_modification": "hands_on_hips",
            },
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Front knee flexion combined with external hip rotation can strain the " "medial collateral ligament (MCL).",
                "recommended_modification": "shorten_stance",
            },
        ],
        "client_id": "p_warrior_2_right",
        "category": "standing",
        "common_mistakes": ["Leaning the torso over the front leg", "Front knee collapsing inward past the big toe", "Shrugging the shoulders"],
        "contraindications": [
            {
                "action": "caution",
                "condition": "vertigo",
                "reason": "Turning the head sharply over the front hand can trigger dizziness.",
                "recommended_modification": "neutral_neck",
            }
        ],
        "drishti": {"alternatives": ["side_wall"], "primary": "front_middle_finger"},
        "modifications": [
            {"instruction": "Rest your hands on your hips to release tension in the shoulders and " "neck.", "name": "Hands on Hips", "target_area": "shoulders"},
            {"instruction": "Keep your chest and gaze facing the side of the room rather than " "turning your head.", "name": "Neutral Neck", "target_area": "neck"},
        ],
        "name": {"aliases": ["Warrior II Right"], "english": "Warrior 2 (Right Leg Forward)", "sanskrit": "Virabhadrasana II"},
        "pose_intent": ["Open the hips and groin", "Strengthen the legs and ankles", "Build stamina and concentration"],
        "progression": {
            "advanced": "Deepest expression with perfect external rotation of the front hip.",
            "beginner": "Shorter stance, shallow bend in the front knee.",
            "intermediate": "Front thigh parallel to the floor, arms actively reaching apart.",
        },
        "sensory_cues": [
            {"area": "arms", "cue": "Imagine your arms are being gently pulled in opposite directions."},
            {"area": "legs", "cue": "Feel the power and stability in your legs."},
        ],
        "typical_entries": ["p_warrior_1_right", "p_downward_dog", "p_mountain"],
        "typical_exits": ["p_triangle_right", "p_plank"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_warrior_3_right"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 5,
            "balance_requirement": 5,
            "muscular_load": {"core": 4, "upper_body": 3, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 2, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Lifting the back leg without core engagement hyperextends the lumbar spine.",
                "recommended_modification": "hands_on_blocks",
            },
            {"action": "modify", "condition": "ankle_stiffness", "reason": "Requires immense stability from the standing ankle.", "recommended_modification": "wall_support"},
        ],
        "client_id": "p_warrior_3_left",
        "category": "standing",
        "common_mistakes": ["Opening the lifted hip toward the ceiling", "Locking the standing knee", "Dropping the chest below the hips"],
        "contraindications": [
            {"action": "caution", "condition": "hypertension", "reason": "Intense full-body isometric contraction.", "recommended_modification": "airplane_arms"}
        ],
        "drishti": {"alternatives": ["slightly_forward"], "primary": "floor_straight_down"},
        "modifications": [
            {"instruction": "Place your hands on tall yoga blocks directly under your shoulders " "for support.", "name": "Hands on Blocks", "target_area": "lower_back"},
            {"instruction": "Reach your arms back alongside your hips like airplane wings.", "name": "Airplane Arms", "target_area": "shoulders"},
        ],
        "name": {"aliases": ["Warrior III Left", "Flying Warrior"], "english": "Warrior 3 (Left Leg Forward)", "sanskrit": "Virabhadrasana III"},
        "pose_intent": ["Improve balance and proprioception", "Strengthen the standing leg, ankle, and core", "Tone the entire posterior chain"],
        "progression": {
            "advanced": "Arms reaching straight forward, biceps by the ears, forming a perfect 'T'.",
            "beginner": "Hands on blocks or a wall, back leg lifted halfway.",
            "intermediate": "Airplane arms, torso and back leg parallel to the floor.",
        },
        "sensory_cues": [
            {"area": "full_body", "cue": "Imagine a straight line of energy from your back heel through the crown of " "your head."},
            {"area": "feet", "cue": "Feel your standing foot gripping the mat for stability."},
        ],
        "typical_entries": ["p_warrior_1_left", "p_tree_left"],
        "typical_exits": ["p_mountain"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_warrior_3_left"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 5,
            "balance_requirement": 5,
            "muscular_load": {"core": 4, "upper_body": 3, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 2, "spine": 1, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Lifting the back leg without core engagement hyperextends the lumbar spine.",
                "recommended_modification": "hands_on_blocks",
            },
            {"action": "modify", "condition": "ankle_stiffness", "reason": "Requires immense stability from the standing ankle.", "recommended_modification": "wall_support"},
        ],
        "client_id": "p_warrior_3_right",
        "category": "standing",
        "common_mistakes": ["Opening the lifted hip toward the ceiling", "Locking the standing knee", "Dropping the chest below the hips"],
        "contraindications": [
            {"action": "caution", "condition": "hypertension", "reason": "Intense full-body isometric contraction.", "recommended_modification": "airplane_arms"}
        ],
        "drishti": {"alternatives": ["slightly_forward"], "primary": "floor_straight_down"},
        "modifications": [
            {"instruction": "Place your hands on tall yoga blocks directly under your shoulders " "for support.", "name": "Hands on Blocks", "target_area": "lower_back"},
            {"instruction": "Reach your arms back alongside your hips like airplane wings.", "name": "Airplane Arms", "target_area": "shoulders"},
        ],
        "name": {"aliases": ["Warrior III Right", "Flying Warrior"], "english": "Warrior 3 (Right Leg Forward)", "sanskrit": "Virabhadrasana III"},
        "pose_intent": ["Improve balance and proprioception", "Strengthen the standing leg, ankle, and core", "Tone the entire posterior chain"],
        "progression": {
            "advanced": "Arms reaching straight forward, biceps by the ears, forming a perfect 'T'.",
            "beginner": "Hands on blocks or a wall, back leg lifted halfway.",
            "intermediate": "Airplane arms, torso and back leg parallel to the floor.",
        },
        "sensory_cues": [
            {"area": "full_body", "cue": "Imagine a straight line of energy from your back heel through the crown of " "your head."},
            {"area": "feet", "cue": "Feel your standing foot gripping the mat for stability."},
        ],
        "typical_entries": ["p_warrior_1_right", "p_tree_right"],
        "typical_exits": ["p_mountain"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "lateral_flexion", "weight_bearing_points": ["feet", "bottom_hand_optional"], "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_triangle_right"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 2},
            "mobility_load": {"posterior_chain": 4, "hips_and_pelvis": 4, "spine": 3, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Forcing the hand to the floor rounds the spine and strains the hamstring " "attachment.",
                "recommended_modification": "hand_on_shin_or_block",
            },
            {"action": "adjust", "condition": "knee_pain", "reason": "Hyperextension of the front knee.", "recommended_modification": "microbend_front_knee"},
        ],
        "client_id": "p_triangle_left",
        "category": "standing",
        "common_mistakes": ["Resting the hand directly on the knee joint", "Collapsing the top shoulder forward", "Hyperextending (locking) the front knee"],
        "contraindications": [
            {"action": "modify", "condition": "neck_injury", "reason": "Looking up at the top hand strains the cervical spine.", "recommended_modification": "look_down"}
        ],
        "drishti": {"alternatives": ["bottom_foot", "straight_ahead"], "primary": "top_thumb"},
        "modifications": [
            {"instruction": "Rest your bottom hand lightly on a block or your shin, never directly " "on your knee.", "name": "Hand on Block", "target_area": "hamstrings"},
            {"instruction": "Keep your gaze down at your front foot to relax your neck.", "name": "Look Down", "target_area": "neck"},
        ],
        "name": {"aliases": ["Extended Triangle Left"], "english": "Triangle Pose (Left Leg Forward)", "sanskrit": "Trikonasana"},
        "pose_intent": ["Stretch the hamstrings, groin, and hips", "Open the chest and shoulders", "Strengthen the legs and core"],
        "progression": {
            "advanced": "Bottom hand outside the foot on the floor, core holding the torso without " "dumping weight into the hand.",
            "beginner": "Hand high on the shin, slight bend in the front knee.",
            "intermediate": "Hand on a block or ankle, top arm reaching straight up.",
        },
        "sensory_cues": [
            {"area": "ribs", "cue": "Feel the deep stretch along the side of your body."},
            {"area": "spine", "cue": "Imagine leaning back against an invisible wall."},
        ],
        "typical_entries": ["p_warrior_2_left"],
        "typical_exits": ["p_warrior_2_left"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "lateral_flexion", "weight_bearing_points": ["feet", "bottom_hand_optional"], "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_triangle_left"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 2},
            "mobility_load": {"posterior_chain": 4, "hips_and_pelvis": 4, "spine": 3, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Forcing the hand to the floor rounds the spine and strains the hamstring " "attachment.",
                "recommended_modification": "hand_on_shin_or_block",
            },
            {"action": "adjust", "condition": "knee_pain", "reason": "Hyperextension of the front knee.", "recommended_modification": "microbend_front_knee"},
        ],
        "client_id": "p_triangle_right",
        "category": "standing",
        "common_mistakes": ["Resting the hand directly on the knee joint", "Collapsing the top shoulder forward", "Hyperextending (locking) the front knee"],
        "contraindications": [
            {"action": "modify", "condition": "neck_injury", "reason": "Looking up at the top hand strains the cervical spine.", "recommended_modification": "look_down"}
        ],
        "drishti": {"alternatives": ["bottom_foot", "straight_ahead"], "primary": "top_thumb"},
        "modifications": [
            {"instruction": "Rest your bottom hand lightly on a block or your shin, never directly " "on your knee.", "name": "Hand on Block", "target_area": "hamstrings"},
            {"instruction": "Keep your gaze down at your front foot to relax your neck.", "name": "Look Down", "target_area": "neck"},
        ],
        "name": {"aliases": ["Extended Triangle Right"], "english": "Triangle Pose (Right Leg Forward)", "sanskrit": "Trikonasana"},
        "pose_intent": ["Stretch the hamstrings, groin, and hips", "Open the chest and shoulders", "Strengthen the legs and core"],
        "progression": {
            "advanced": "Bottom hand outside the foot on the floor, core holding the torso without " "dumping weight into the hand.",
            "beginner": "Hand high on the shin, slight bend in the front knee.",
            "intermediate": "Hand on a block or ankle, top arm reaching straight up.",
        },
        "sensory_cues": [
            {"area": "ribs", "cue": "Feel the deep stretch along the side of your body."},
            {"area": "spine", "cue": "Imagine leaning back against an invisible wall."},
        ],
        "typical_entries": ["p_warrior_2_right"],
        "typical_exits": ["p_warrior_2_right"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_tree_right"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 4,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 2},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 3, "spine": 1, "shoulders_and_chest": 1},
        },
        "chronic_pain": [
            {
                "action": "avoid_specific_placement",
                "condition": "knee_pain",
                "reason": "Pressing the foot directly against the inner knee joint forces it laterally " "out of alignment.",
                "recommended_modification": "foot_below_knee",
            }
        ],
        "client_id": "p_tree_left",
        "category": "standing",
        "common_mistakes": ["Placing the foot directly on the knee joint", "Sinking the hip of the standing leg out to the side", "Holding the breath while balancing"],
        "contraindications": [
            {"action": "modify", "condition": "vertigo", "reason": "Standing on one leg challenges the vestibular system.", "recommended_modification": "kickstand_foot"}
        ],
        "drishti": {"alternatives": ["upward"], "primary": "steady_point_forward"},
        "modifications": [
            {"instruction": "Keep your toes on the floor and rest your heel against your inner " "ankle.", "name": "Kickstand", "target_area": "balance"},
            {"instruction": "Place your foot flat against your inner calf, completely avoiding the " "knee joint.", "name": "Foot Below Knee", "target_area": "knees"},
        ],
        "name": {"aliases": [], "english": "Tree Pose (Left Leg Lifted)", "sanskrit": "Vrksasana"},
        "pose_intent": ["Improve balance and focus", "Strengthen the standing leg and ankle", "Externally rotate and open the hip"],
        "progression": {
            "advanced": "Foot high on the inner thigh, gaze lifted or eyes closed.",
            "beginner": "Kickstand variation, hands at the heart.",
            "intermediate": "Foot on the inner calf or thigh, arms growing overhead.",
        },
        "sensory_cues": [
            {"area": "legs", "cue": "Press your foot into your leg, and your leg equally back into your foot."},
            {"area": "spine", "cue": "Feel yourself rooted to the floor, yet growing taller through your spine."},
        ],
        "typical_entries": ["p_mountain"],
        "typical_exits": ["p_mountain", "p_warrior_3_left"],
    },
    {
        "anatomical_signature": {"is_inverted": False, "spinal_shape": "neutral", "weight_bearing_points": ["feet"], "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_tree_left"}, "requires_counter_pose": False, "recommended_counter_poses": []},
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 4,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 2},
            "mobility_load": {"posterior_chain": 1, "hips_and_pelvis": 3, "spine": 1, "shoulders_and_chest": 1},
        },
        "chronic_pain": [
            {
                "action": "avoid_specific_placement",
                "condition": "knee_pain",
                "reason": "Pressing the foot directly against the inner knee joint forces it laterally " "out of alignment.",
                "recommended_modification": "foot_below_knee",
            }
        ],
        "client_id": "p_tree_right",
        "category": "standing",
        "common_mistakes": ["Placing the foot directly on the knee joint", "Sinking the hip of the standing leg out to the side", "Holding the breath while balancing"],
        "contraindications": [
            {"action": "modify", "condition": "vertigo", "reason": "Standing on one leg challenges the vestibular system.", "recommended_modification": "kickstand_foot"}
        ],
        "drishti": {"alternatives": ["upward"], "primary": "steady_point_forward"},
        "modifications": [
            {"instruction": "Keep your toes on the floor and rest your heel against your inner " "ankle.", "name": "Kickstand", "target_area": "balance"},
            {"instruction": "Place your foot flat against your inner calf, completely avoiding the " "knee joint.", "name": "Foot Below Knee", "target_area": "knees"},
        ],
        "name": {"aliases": [], "english": "Tree Pose (Right Leg Lifted)", "sanskrit": "Vrksasana"},
        "pose_intent": ["Improve balance and focus", "Strengthen the standing leg and ankle", "Externally rotate and open the hip"],
        "progression": {
            "advanced": "Foot high on the inner thigh, gaze lifted or eyes closed.",
            "beginner": "Kickstand variation, hands at the heart.",
            "intermediate": "Foot on the inner calf or thigh, arms growing overhead.",
        },
        "sensory_cues": [
            {"area": "legs", "cue": "Press your foot into your leg, and your leg equally back into your foot."},
            {"area": "spine", "cue": "Feel yourself rooted to the floor, yet growing taller through your spine."},
        ],
        "typical_entries": ["p_mountain"],
        "typical_exits": ["p_mountain", "p_warrior_3_right"],
    },
]
