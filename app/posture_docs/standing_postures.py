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
        "name": "Mountain Pose",
        "sanskrit_name": "Tadasana",
        "aliases": ["Samasthiti", "Standing Pose"],
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
        "typical_exits": ["p_upward_salute", "p_chair", "p_forward_fold", "p_tree_left", "p_tree_right", "p_garland_pose"],
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
        "name": "Upward Salute",
        "sanskrit_name": "Urdhva Hastasana",
        "aliases": ["Raised Hands Pose"],
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
        "name": "Chair Pose",
        "sanskrit_name": "Utkatasana",
        "aliases": ["Fierce Pose", "Lightning Bolt Pose"],
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
        "name": "Standing Forward Fold",
        "sanskrit_name": "Uttanasana",
        "aliases": ["Standing Forward Bend"],
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
        "typical_exits": ["p_halfway_lift", "p_plank", "p_mountain", "p_garland_pose", "p_low_lunge_left", "p_low_lunge_right"],
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
        "name": "Halfway Lift",
        "sanskrit_name": "Ardha Uttanasana",
        "aliases": ["Standing Half Forward Bend"],
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
        "name": "Warrior 1 (Left Leg Forward)",
        "sanskrit_name": "Virabhadrasana I",
        "aliases": ["Warrior I Left"],
        "pose_intent": ["Strengthen quadriceps, glutes, and ankles", "Stretch the hip flexors of the back leg", "Open the chest and shoulders"],
        "progression": {
            "advanced": "Palms touching overhead, gaze up, back leg perfectly straight.",
            "beginner": "Short stance, hands on hips.",
            "intermediate": "Deepen the front knee bend to 90 degrees, arms overhead.",
        },
        "sensory_cues": [{"area": "feet", "cue": "Feel your back heel anchoring you down."}, {"area": "hips", "cue": "Notice the stretch across the front of your back hip."}],
        "typical_entries": ["p_downward_dog", "p_mountain"],
        "typical_exits": ["p_warrior_2_left", "p_plank", "p_mountain", "p_low_lunge_left"],
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
        "name": "Warrior 1 (Right Leg Forward)",
        "sanskrit_name": "Virabhadrasana I",
        "aliases": ["Warrior I Right"],
        "pose_intent": ["Strengthen quadriceps, glutes, and ankles", "Stretch the hip flexors of the back leg", "Open the chest and shoulders"],
        "progression": {
            "advanced": "Palms touching overhead, gaze up, back leg perfectly straight.",
            "beginner": "Short stance, hands on hips.",
            "intermediate": "Deepen the front knee bend to 90 degrees, arms overhead.",
        },
        "sensory_cues": [{"area": "feet", "cue": "Feel your back heel anchoring you down."}, {"area": "hips", "cue": "Notice the stretch across the front of your back hip."}],
        "typical_entries": ["p_downward_dog", "p_mountain"],
        "typical_exits": ["p_warrior_2_right", "p_plank", "p_mountain", "p_low_lunge_right"],
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
        "name": "Warrior 2 (Left Leg Forward)",
        "sanskrit_name": "Virabhadrasana II",
        "aliases": ["Warrior II Left"],
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
        "typical_exits": [
            "p_triangle_left",
            "p_extended_side_angle_left",
            "p_reverse_warrior_left",
            "p_plank",
            "p_warrior_2_right",
        ],
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
        "name": "Warrior 2 (Right Leg Forward)",
        "sanskrit_name": "Virabhadrasana II",
        "aliases": ["Warrior II Right"],
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
        "typical_exits": [
            "p_triangle_right",
            "p_extended_side_angle_right",
            "p_reverse_warrior_right",
            "p_plank",
            "p_warrior_2_left",
        ],
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
        "name": "Warrior 3 (Left Leg Forward)",
        "sanskrit_name": "Virabhadrasana III",
        "aliases": ["Warrior III Left", "Flying Warrior"],
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
        "typical_entries": ["p_warrior_1_left", "p_tree_left", "p_low_lunge_left"],
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
        "name": "Warrior 3 (Right Leg Forward)",
        "sanskrit_name": "Virabhadrasana III",
        "aliases": ["Warrior III Right", "Flying Warrior"],
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
        "typical_entries": ["p_warrior_1_right", "p_tree_right", "p_low_lunge_right"],
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
        "name": "Triangle Pose (Left Leg Forward)",
        "sanskrit_name": "Trikonasana",
        "aliases": ["Extended Triangle Left"],
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
        "typical_entries": ["p_warrior_2_left", "p_extended_side_angle_left"],
        "typical_exits": [
            "p_warrior_2_left",
            "p_half_moon_left",
            "p_extended_side_angle_left",
            "p_triangle_right",
        ],
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
        "name": "Triangle Pose (Right Leg Forward)",
        "sanskrit_name": "Trikonasana",
        "aliases": ["Extended Triangle Right"],
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
        "typical_entries": ["p_warrior_2_right", "p_extended_side_angle_right"],
        "typical_exits": [
            "p_warrior_2_right",
            "p_half_moon_right",
            "p_extended_side_angle_right",
            "p_triangle_left",
        ],
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
        "name": "Tree Pose (Left Leg Lifted)",
        "sanskrit_name": "Vrksasana",
        "aliases": [],
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
        "name": "Tree Pose (Right Leg Lifted)",
        "sanskrit_name": "Vrksasana",
        "aliases": [],
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
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "flexion",
            "weight_bearing_points": ["feet", "heels"],
            "laterality": {"type": "symmetrical", "active_side": "neutral"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 1, "lower_body": 4},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 4, "spine": 2, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Deep flexion and ankle dorsiflexion load the patellar tendon.",
                "recommended_modification": "heels_on_blanket",
            },
            {
                "action": "modify",
                "condition": "lower_back_pain",
                "reason": "Rounding in the squat can strain the lumbar spine.",
                "recommended_modification": "torso_on_thighs",
            },
        ],
        "client_id": "p_garland_pose",
        "category": "standing",
        "common_mistakes": [
            "Collapsing the chest forward",
            "Lifting the heels when the ankles are tight",
            "Knees buckling inward",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "knee_injury",
                "reason": "Deep knee flexion under load can aggravate meniscus issues.",
                "recommended_modification": "supported_squat",
            }
        ],
        "drishti": {"alternatives": ["closed_eyes"], "primary": "straight_ahead"},
        "modifications": [
            {
                "instruction": "Slide a rolled blanket under your heels if they do not reach the " "floor.",
                "name": "Heels on Blanket",
                "target_area": "ankles",
            },
            {
                "instruction": "Sit on a block between your feet to reduce depth in the knees and " "hips.",
                "name": "Supported Squat",
                "target_area": "knees",
            },
        ],
        "name": "Garland Pose",
        "sanskrit_name": "Malasana",
        "aliases": ["Yogi Squat"],
        "pose_intent": ["Open the hips, groin, and ankles", "Strengthen the legs and pelvic floor", "Prepare the body for forward folds"],
        "progression": {
            "advanced": "Hands in prayer at the heart with elbows pressing the thighs open.",
            "beginner": "Heels lifted, sitting on a block.",
            "intermediate": "Heels grounded, spine long, arms inside the knees.",
        },
        "sensory_cues": [
            {"area": "feet", "cue": "Spread your toes and root evenly through the soles."},
            {"area": "spine", "cue": "Grow tall through the crown even as you sink the hips."},
        ],
        "typical_entries": ["p_mountain", "p_forward_fold", "p_chair"],
        "typical_exits": ["p_mountain", "p_forward_fold", "p_downward_dog"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "mild_extension",
            "weight_bearing_points": ["feet", "back_knee"],
            "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_low_lunge_right"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 4, "spine": 2, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Shear force on the back kneecap against the floor.",
                "recommended_modification": "pad_back_knee",
            }
        ],
        "client_id": "p_low_lunge_left",
        "category": "standing",
        "common_mistakes": [
            "Collapsing weight into the front knee",
            "Sinking the lower back",
            "Front knee drifting inward past the ankle",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "ankle_stiffness",
                "reason": "Limited dorsiflexion strains the front knee.",
                "recommended_modification": "block_under_front_foot",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "forward_horizon"},
        "modifications": [
            {
                "instruction": "Fold a blanket and place it under your back knee for cushioning.",
                "name": "Pad Back Knee",
                "target_area": "knees",
            },
            {
                "instruction": "Place your front foot on a folded blanket to lift the heel.",
                "name": "Block Under Front Foot",
                "target_area": "ankles",
            },
        ],
        "name": "Low Lunge (Left Leg Forward)",
        "sanskrit_name": "Anjaneyasana",
        "aliases": ["Crescent Lunge (Knee Down)", "Runner's Lunge"],
        "pose_intent": ["Stretch the hip flexors of the back leg", "Open the chest and shoulders", "Prepare for Warrior 1 or high lunge"],
        "progression": {
            "advanced": "Sink the hips square while lifting the torso vertical with arms overhead.",
            "beginner": "Hands on blocks framing the front foot.",
            "intermediate": "Hands on the front thigh or reaching overhead.",
        },
        "sensory_cues": [
            {"area": "hips", "cue": "Draw the front hip back and the back hip forward to square the pelvis."},
            {"area": "ribs", "cue": "Lift the ribcage away from the waist to lengthen the spine."},
        ],
        "typical_entries": ["p_downward_dog", "p_forward_fold"],
        "typical_exits": ["p_warrior_1_left", "p_downward_dog", "p_low_lunge_right"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "mild_extension",
            "weight_bearing_points": ["feet", "back_knee"],
            "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_low_lunge_left"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 4, "spine": 2, "shoulders_and_chest": 2},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "knee_pain",
                "reason": "Shear force on the back kneecap against the floor.",
                "recommended_modification": "pad_back_knee",
            }
        ],
        "client_id": "p_low_lunge_right",
        "category": "standing",
        "common_mistakes": [
            "Collapsing weight into the front knee",
            "Sinking the lower back",
            "Front knee drifting inward past the ankle",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "ankle_stiffness",
                "reason": "Limited dorsiflexion strains the front knee.",
                "recommended_modification": "block_under_front_foot",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "forward_horizon"},
        "modifications": [
            {
                "instruction": "Fold a blanket and place it under your back knee for cushioning.",
                "name": "Pad Back Knee",
                "target_area": "knees",
            },
            {
                "instruction": "Place your front foot on a folded blanket to lift the heel.",
                "name": "Block Under Front Foot",
                "target_area": "ankles",
            },
        ],
        "name": "Low Lunge (Right Leg Forward)",
        "sanskrit_name": "Anjaneyasana",
        "aliases": ["Crescent Lunge (Knee Down)", "Runner's Lunge"],
        "pose_intent": ["Stretch the hip flexors of the back leg", "Open the chest and shoulders", "Prepare for Warrior 1 or high lunge"],
        "progression": {
            "advanced": "Sink the hips square while lifting the torso vertical with arms overhead.",
            "beginner": "Hands on blocks framing the front foot.",
            "intermediate": "Hands on the front thigh or reaching overhead.",
        },
        "sensory_cues": [
            {"area": "hips", "cue": "Draw the front hip back and the back hip forward to square the pelvis."},
            {"area": "ribs", "cue": "Lift the ribcage away from the waist to lengthen the spine."},
        ],
        "typical_entries": ["p_downward_dog", "p_forward_fold"],
        "typical_exits": ["p_warrior_1_right", "p_downward_dog", "p_low_lunge_left"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "lateral_flexion",
            "weight_bearing_points": ["feet", "bottom_arm_optional"],
            "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_extended_side_angle_right"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 3, "lower_body": 4},
            "mobility_load": {"posterior_chain": 3, "hips_and_pelvis": 4, "spine": 3, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Short stance forces rounding and side-bend into the lower back.",
                "recommended_modification": "forearm_on_thigh",
            }
        ],
        "client_id": "p_extended_side_angle_left",
        "category": "standing",
        "common_mistakes": [
            "Collapsing the chest toward the floor",
            "Front knee caving inward",
            "Resting all weight into the bottom hand",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "neck_injury",
                "reason": "Looking up under the arm strains rotation.",
                "recommended_modification": "gaze_down",
            }
        ],
        "drishti": {"alternatives": ["side_wall"], "primary": "under_arm"},
        "modifications": [
            {
                "instruction": "Rest your forearm on your front thigh instead of placing the hand on " "the floor.",
                "name": "Forearm on Thigh",
                "target_area": "lower_back",
            },
            {"instruction": "Keep your gaze toward the floor to keep the neck neutral.", "name": "Gaze Down", "target_area": "neck"},
        ],
        "name": "Extended Side Angle Pose (Left Leg Forward)",
        "sanskrit_name": "Utthita Parsvakonasana",
        "aliases": ["Side Angle Pose Left"],
        "pose_intent": ["Strengthen the legs and side waist", "Open the chest and groin", "Build stamina in standing poses"],
        "progression": {
            "advanced": "Bind the hands behind the back or under the front thigh.",
            "beginner": "Shorten the stance and use a block under the bottom hand.",
            "intermediate": "Top arm extended by the ear in one long line from heel to fingertips.",
        },
        "sensory_cues": [
            {"area": "ribs", "cue": "Rotate the underside ribs up toward the ceiling."},
            {"area": "legs", "cue": "Press the outer edge of the back foot firmly down."},
        ],
        "typical_entries": ["p_warrior_2_left", "p_low_lunge_left"],
        "typical_exits": [
            "p_warrior_2_left",
            "p_reverse_warrior_left",
            "p_triangle_left",
            "p_half_moon_left",
            "p_extended_side_angle_right",
        ],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "lateral_flexion",
            "weight_bearing_points": ["feet", "bottom_arm_optional"],
            "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_extended_side_angle_left"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 3, "lower_body": 4},
            "mobility_load": {"posterior_chain": 3, "hips_and_pelvis": 4, "spine": 3, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "tight_hamstrings",
                "reason": "Short stance forces rounding and side-bend into the lower back.",
                "recommended_modification": "forearm_on_thigh",
            }
        ],
        "client_id": "p_extended_side_angle_right",
        "category": "standing",
        "common_mistakes": [
            "Collapsing the chest toward the floor",
            "Front knee caving inward",
            "Resting all weight into the bottom hand",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "neck_injury",
                "reason": "Looking up under the arm strains rotation.",
                "recommended_modification": "gaze_down",
            }
        ],
        "drishti": {"alternatives": ["side_wall"], "primary": "under_arm"},
        "modifications": [
            {
                "instruction": "Rest your forearm on your front thigh instead of placing the hand on " "the floor.",
                "name": "Forearm on Thigh",
                "target_area": "lower_back",
            },
            {"instruction": "Keep your gaze toward the floor to keep the neck neutral.", "name": "Gaze Down", "target_area": "neck"},
        ],
        "name": "Extended Side Angle Pose (Right Leg Forward)",
        "sanskrit_name": "Utthita Parsvakonasana",
        "aliases": ["Side Angle Pose Right"],
        "pose_intent": ["Strengthen the legs and side waist", "Open the chest and groin", "Build stamina in standing poses"],
        "progression": {
            "advanced": "Bind the hands behind the back or under the front thigh.",
            "beginner": "Shorten the stance and use a block under the bottom hand.",
            "intermediate": "Top arm extended by the ear in one long line from heel to fingertips.",
        },
        "sensory_cues": [
            {"area": "ribs", "cue": "Rotate the underside ribs up toward the ceiling."},
            {"area": "legs", "cue": "Press the outer edge of the back foot firmly down."},
        ],
        "typical_entries": ["p_warrior_2_right", "p_low_lunge_right"],
        "typical_exits": [
            "p_warrior_2_right",
            "p_reverse_warrior_right",
            "p_triangle_right",
            "p_half_moon_right",
            "p_extended_side_angle_left",
        ],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "lateral_flexion",
            "weight_bearing_points": ["feet"],
            "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_reverse_warrior_right"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 2, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "shoulder_pain",
                "reason": "The long side reach can irritate the rotator cuff.",
                "recommended_modification": "hand_on_hip",
            }
        ],
        "client_id": "p_reverse_warrior_left",
        "category": "standing",
        "common_mistakes": [
            "Leaning the torso backward instead of laterally",
            "Bending the front knee past 90 degrees",
            "Compressing the side of the neck",
        ],
        "contraindications": [
            {
                "action": "caution",
                "condition": "vertigo",
                "reason": "Side bending with the gaze up can disturb balance.",
                "recommended_modification": "eyes_forward",
            }
        ],
        "drishti": {"alternatives": ["side_wall"], "primary": "top_hand"},
        "modifications": [
            {"instruction": "Rest your top hand on your hip to shorten the lever of the side bend.", "name": "Hand on Hip", "target_area": "shoulders"},
        ],
        "name": "Reverse Warrior Pose (Left Leg Forward)",
        "sanskrit_name": "Viparita Virabhadrasana",
        "aliases": ["Peaceful Warrior Left"],
        "pose_intent": ["Lengthen the side waist", "Open the chest and intercostals", "Link breath with lateral movement"],
        "progression": {
            "advanced": "Deep side bend while keeping the front thigh parallel to the floor.",
            "beginner": "Shallow side bend with a shorter stance.",
            "intermediate": "Smooth transition from Warrior 2 into Reverse Warrior on the exhale.",
        },
        "sensory_cues": [
            {"area": "ribs", "cue": "Feel length from the outer hip to the fingertips."},
            {"area": "legs", "cue": "Anchor through the outer edge of the back foot."},
        ],
        "typical_entries": ["p_warrior_2_left", "p_extended_side_angle_left"],
        "typical_exits": ["p_warrior_2_left", "p_extended_side_angle_left", "p_triangle_left"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "lateral_flexion",
            "weight_bearing_points": ["feet"],
            "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_reverse_warrior_left"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 3,
            "balance_requirement": 2,
            "muscular_load": {"core": 2, "upper_body": 2, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 2, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "shoulder_pain",
                "reason": "The long side reach can irritate the rotator cuff.",
                "recommended_modification": "hand_on_hip",
            }
        ],
        "client_id": "p_reverse_warrior_right",
        "category": "standing",
        "common_mistakes": [
            "Leaning the torso backward instead of laterally",
            "Bending the front knee past 90 degrees",
            "Compressing the side of the neck",
        ],
        "contraindications": [
            {
                "action": "caution",
                "condition": "vertigo",
                "reason": "Side bending with the gaze up can disturb balance.",
                "recommended_modification": "eyes_forward",
            }
        ],
        "drishti": {"alternatives": ["side_wall"], "primary": "top_hand"},
        "modifications": [
            {"instruction": "Rest your top hand on your hip to shorten the lever of the side bend.", "name": "Hand on Hip", "target_area": "shoulders"},
        ],
        "name": "Reverse Warrior Pose (Right Leg Forward)",
        "sanskrit_name": "Viparita Virabhadrasana",
        "aliases": ["Peaceful Warrior Right"],
        "pose_intent": ["Lengthen the side waist", "Open the chest and intercostals", "Link breath with lateral movement"],
        "progression": {
            "advanced": "Deep side bend while keeping the front thigh parallel to the floor.",
            "beginner": "Shallow side bend with a shorter stance.",
            "intermediate": "Smooth transition from Warrior 2 into Reverse Warrior on the exhale.",
        },
        "sensory_cues": [
            {"area": "ribs", "cue": "Feel length from the outer hip to the fingertips."},
            {"area": "legs", "cue": "Anchor through the outer edge of the back foot."},
        ],
        "typical_entries": ["p_warrior_2_right", "p_extended_side_angle_right"],
        "typical_exits": ["p_warrior_2_right", "p_extended_side_angle_right", "p_triangle_right"],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "neutral",
            "weight_bearing_points": ["standing_foot", "bottom_hand_optional"],
            "laterality": {"type": "asymmetrical", "active_side": "left", "paired_pose": "p_half_moon_right"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 5,
            "muscular_load": {"core": 4, "upper_body": 3, "lower_body": 3},
            "mobility_load": {"posterior_chain": 3, "hips_and_pelvis": 3, "spine": 2, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Rotating the open hip upward can torque the lumbar spine.",
                "recommended_modification": "hand_on_block",
            }
        ],
        "client_id": "p_half_moon_left",
        "category": "standing",
        "common_mistakes": [
            "Dropping the chest toward the floor",
            "Hyperextending the standing knee",
            "Turning the lifted hip too far open",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "vertigo",
                "reason": "Single-leg balance with head rotation challenges equilibrium.",
                "recommended_modification": "wall_support",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "top_hand"},
        "modifications": [
            {
                "instruction": "Place your bottom hand on a block under the shoulder to lift the " "torso.",
                "name": "Hand on Block",
                "target_area": "lower_back",
            },
            {
                "instruction": "Stand with your back foot against a wall for balance support.",
                "name": "Wall Support",
                "target_area": "balance",
            },
        ],
        "name": "Half Moon Pose (Left Leg Standing)",
        "sanskrit_name": "Ardha Chandrasana",
        "aliases": ["Half Moon Left"],
        "pose_intent": ["Improve balance and proprioception", "Strengthen the standing leg and gluteus medius", "Open the hips and chest in rotation"],
        "progression": {
            "advanced": "Gaze upward toward the top hand with the arms in one vertical line.",
            "beginner": "Use a wall or chair for the lifted leg and hand.",
            "intermediate": "Float the top leg parallel to the floor with flexed foot.",
        },
        "sensory_cues": [
            {"area": "standing_leg", "cue": "Micro-bend the knee without locking as you press through the heel and " "ball of the foot."},
            {"area": "torso", "cue": "Stack shoulders over hips like a sideways Tadasana."},
        ],
        "typical_entries": ["p_triangle_left", "p_extended_side_angle_left"],
        "typical_exits": [
            "p_triangle_left",
            "p_warrior_2_left",
            "p_side_plank_left",
            "p_mountain",
        ],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "neutral",
            "weight_bearing_points": ["standing_foot", "bottom_hand_optional"],
            "laterality": {"type": "asymmetrical", "active_side": "right", "paired_pose": "p_half_moon_left"},
            "requires_counter_pose": False,
            "recommended_counter_poses": [],
        },
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 5,
            "muscular_load": {"core": 4, "upper_body": 3, "lower_body": 3},
            "mobility_load": {"posterior_chain": 3, "hips_and_pelvis": 3, "spine": 2, "shoulders_and_chest": 3},
        },
        "chronic_pain": [
            {
                "action": "adjust",
                "condition": "lower_back_pain",
                "reason": "Rotating the open hip upward can torque the lumbar spine.",
                "recommended_modification": "hand_on_block",
            }
        ],
        "client_id": "p_half_moon_right",
        "category": "standing",
        "common_mistakes": [
            "Dropping the chest toward the floor",
            "Hyperextending the standing knee",
            "Turning the lifted hip too far open",
        ],
        "contraindications": [
            {
                "action": "modify",
                "condition": "vertigo",
                "reason": "Single-leg balance with head rotation challenges equilibrium.",
                "recommended_modification": "wall_support",
            }
        ],
        "drishti": {"alternatives": ["straight_ahead"], "primary": "top_hand"},
        "modifications": [
            {
                "instruction": "Place your bottom hand on a block under the shoulder to lift the " "torso.",
                "name": "Hand on Block",
                "target_area": "lower_back",
            },
            {
                "instruction": "Stand with your back foot against a wall for balance support.",
                "name": "Wall Support",
                "target_area": "balance",
            },
        ],
        "name": "Half Moon Pose (Right Leg Standing)",
        "sanskrit_name": "Ardha Chandrasana",
        "aliases": ["Half Moon Right"],
        "pose_intent": ["Improve balance and proprioception", "Strengthen the standing leg and gluteus medius", "Open the hips and chest in rotation"],
        "progression": {
            "advanced": "Gaze upward toward the top hand with the arms in one vertical line.",
            "beginner": "Use a wall or chair for the lifted leg and hand.",
            "intermediate": "Float the top leg parallel to the floor with flexed foot.",
        },
        "sensory_cues": [
            {"area": "standing_leg", "cue": "Micro-bend the knee without locking as you press through the heel and " "ball of the foot."},
            {"area": "torso", "cue": "Stack shoulders over hips like a sideways Tadasana."},
        ],
        "typical_entries": ["p_triangle_right", "p_extended_side_angle_right"],
        "typical_exits": [
            "p_triangle_right",
            "p_warrior_2_right",
            "p_side_plank_right",
            "p_mountain",
        ],
    },
    {
        "anatomical_signature": {
            "is_inverted": False,
            "spinal_shape": "extension",
            "weight_bearing_points": ["knees", "shins", "feet", "hands_to_heels"],
            "laterality": {"type": "symmetrical", "active_side": "neutral"},
            "requires_counter_pose": True,
            "recommended_counter_poses": ["p_childs_pose"],
        },
        "intensity_profile": {
            "overall_exertion": 4,
            "balance_requirement": 2,
            "muscular_load": {"core": 3, "upper_body": 2, "lower_body": 3},
            "mobility_load": {"posterior_chain": 2, "hips_and_pelvis": 3, "spine": 5, "shoulders_and_chest": 5},
        },
        "chronic_pain": [
            {
                "action": "modify",
                "condition": "lower_back_pain",
                "reason": "Compression in the lumbar spine if the thighs are not aligned.",
                "recommended_modification": "toes_tucked",
            }
        ],
        "client_id": "p_camel_pose",
        "category": "standing",
        "common_mistakes": [
            "Leading with the head instead of lifting from the sternum",
            "Squeezing the glutes excessively",
            "Knees wider than hips without support",
        ],
        "contraindications": [
            {"action": "avoid", "condition": "neck_injury", "reason": "Extreme cervical extension under load.", "recommended_modification": "chin_to_chest"},
            {
                "action": "modify_or_avoid",
                "condition": "hypertension",
                "reason": "Strong backbend can elevate heart rate and blood pressure.",
                "recommended_modification": "supported_bridge",
            },
        ],
        "drishti": {"alternatives": ["third_eye"], "primary": "ceiling"},
        "modifications": [
            {
                "instruction": "Tuck your toes under to lift the heels closer to your hands.",
                "name": "Toes Tucked",
                "target_area": "lower_back",
            },
            {
                "instruction": "Place blocks beside your ankles and rest your hands on the blocks " "instead of the heels.",
                "name": "Hands on Blocks",
                "target_area": "shoulders",
            },
        ],
        "name": "Camel Pose",
        "sanskrit_name": "Ustrasana",
        "aliases": ["Ustrasana"],
        "pose_intent": ["Open the entire front body", "Stretch hip flexors and abdominals", "Stimulate the respiratory and endocrine systems"],
        "progression": {
            "advanced": "Reach back to grasp the heels with thighs vertical and hips over knees.",
            "beginner": "Hands on the low back for support, minimal backbend.",
            "intermediate": "One hand at a time to each heel with the chest lifting.",
        },
        "sensory_cues": [
            {"area": "heart", "cue": "Lift the sternum first; let the head follow last."},
            {"area": "thighs", "cue": "Hug the inner thighs toward the midline for stability."},
        ],
        "typical_entries": ["p_table_top", "p_childs_pose"],
        "typical_exits": ["p_childs_pose", "p_table_top", "p_forward_fold"],
    },
]
