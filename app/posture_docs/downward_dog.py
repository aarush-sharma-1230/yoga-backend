import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

# --- POSTURES DATA ARRAY (PART 1: Standing & Balancing) ---
# Note: Due to strict output length limits, this array contains the first 10 foundational postures.
# The remaining postures (All-Fours, Prone, Seated, Supine) follow the exact same schema.
postures_data = [
    {
        "client_id": "p_mountain",
        "name": {
            "sanskrit": "Tadasana",
            "english": "Mountain Pose",
            "aliases": ["Samasthiti", "Standing Pose"]
        },
        "typical_entries": ["p_forward_fold", "p_chair_pose"],
        "typical_exits": ["p_upward_salute", "p_chair_pose", "p_forward_fold", "p_tree_pose"],
        "pose_intent": [
            "Establish grounding and physical equilibrium",
            "Improve posture and spinal alignment",
            "Calm the nervous system"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "vertigo",
                "action": "caution",
                "reason": "Closing eyes while standing can cause loss of balance.",
                "recommended_modification": "eyes_open"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Anterior pelvic tilt creates lumbar compression.",
                "recommended_modification": "tuck_tailbone"
            },
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Locking the knees causes joint strain.",
                "recommended_modification": "microbend_knees"
            }
        ],
        "modifications": [
            {
                "name": "Eyes Open",
                "target_area": "full_body",
                "instruction": "Keep your gaze softly focused on a point in front of you."
            },
            {
                "name": "Microbend Knees",
                "target_area": "knees",
                "instruction": "Keep a tiny softness in the back of your knees to engage the quadriceps."
            }
        ],
        "progression": {
            "beginner": "Stand with feet hip-width apart for better balance.",
            "intermediate": "Bring big toes to touch, heels slightly apart.",
            "advanced": "Close eyes and maintain equilibrium relying on internal proprioception."
        },
        "common_mistakes": [
            "Locking the knees",
            "Dumping weight entirely into the heels",
            "Arching the lower back excessively"
        ],
        "sensory_cues": [
            {"cue": "Feel the four corners of your feet rooting deeply into the earth.", "area": "feet"},
            {"cue": "Imagine a string pulling the crown of your head directly up.", "area": "spine"}
        ],
        "drishti": {
            "primary": "straight_ahead",
            "alternatives": ["closed_eyes"]
        }
    },
    {
        "client_id": "p_upward_salute",
        "name": {
            "sanskrit": "Urdhva Hastasana",
            "english": "Upward Salute",
            "aliases": ["Raised Hands Pose"]
        },
        "typical_entries": ["p_mountain"],
        "typical_exits": ["p_forward_fold", "p_chair_pose", "p_mountain"],
        "pose_intent": [
            "Lengthen the lateral sides of the body",
            "Open the chest and shoulders",
            "Stimulate the respiratory system"
        ],
        "anatomical_signature": {
            "spinal_shape": "mild_extension",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "hypertension",
                "action": "modify",
                "reason": "Raising arms overhead can temporarily elevate blood pressure.",
                "recommended_modification": "hands_at_heart"
            }
        ],
        "chronic_pain": [
            {
                "condition": "shoulder_pain",
                "action": "modify",
                "reason": "Shoulder flexion can pinch the subacromial space.",
                "recommended_modification": "cactus_arms"
            },
            {
                "condition": "neck_pain",
                "action": "adjust",
                "reason": "Looking up at the thumbs strains the cervical spine.",
                "recommended_modification": "neutral_neck"
            }
        ],
        "modifications": [
            {
                "name": "Cactus Arms",
                "target_area": "shoulders",
                "instruction": "Bend your elbows to 90 degrees instead of reaching straight up."
            },
            {
                "name": "Neutral Neck",
                "target_area": "neck",
                "instruction": "Keep your gaze straight forward rather than looking up at your hands."
            }
        ],
        "progression": {
            "beginner": "Keep arms shoulder-width apart.",
            "intermediate": "Bring palms to touch overhead.",
            "advanced": "Add a slight upper backbend while keeping the core braced."
        },
        "common_mistakes": [
            "Shrugging shoulders up to the ears",
            "Flaring the lower ribs outward",
            "Craning the neck back excessively"
        ],
        "sensory_cues": [
            {"cue": "Notice the lift from your ribcage as you reach upward.", "area": "torso"},
            {"cue": "Feel the space opening up along your side body.", "area": "ribs"}
        ],
        "drishti": {
            "primary": "thumbs",
            "alternatives": ["straight_ahead"]
        }
    },
    {
        "client_id": "p_chair",
        "name": {
            "sanskrit": "Utkatasana",
            "english": "Chair Pose",
            "aliases": ["Fierce Pose", "Lightning Bolt Pose"]
        },
        "typical_entries": ["p_mountain", "p_upward_salute"],
        "typical_exits": ["p_forward_fold", "p_mountain", "p_halfway_lift"],
        "pose_intent": [
            "Strengthen thighs, calves, and ankles",
            "Engage the core and erector spinae",
            "Build internal heat"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "hypertension",
                "action": "modify",
                "reason": "Arms overhead combined with large muscle engagement increases cardiac load.",
                "recommended_modification": "hands_at_heart"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Deep flexion combined with weight-bearing strains the patellar tendon.",
                "recommended_modification": "shallow_bend"
            },
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Weak core causes the lumbar spine to arch heavily (anterior tilt).",
                "recommended_modification": "tuck_tailbone"
            }
        ],
        "modifications": [
            {
                "name": "Shallow Bend",
                "target_area": "knees",
                "instruction": "Bend your knees only a few inches, keeping the weight entirely in your heels."
            },
            {
                "name": "Hands at Heart",
                "target_area": "shoulders",
                "instruction": "Bring your hands to prayer position at your chest to reduce shoulder and cardiovascular strain."
            }
        ],
        "progression": {
            "beginner": "Feet hip-width apart, shallow bend.",
            "intermediate": "Big toes touching, thighs parallel to the floor.",
            "advanced": "Hold the deep bend while lifting the heels off the floor."
        },
        "common_mistakes": [
            "Knees tracking past the toes",
            "Arching the lower back (duck butt)",
            "Dropping the chest toward the thighs"
        ],
        "sensory_cues": [
            {"cue": "Feel the weight shifting back into your heels.", "area": "feet"},
            {"cue": "Notice the heat building in your quadriceps.", "area": "thighs"}
        ],
        "drishti": {
            "primary": "slightly_upward",
            "alternatives": ["straight_ahead"]
        }
    },
    {
        "client_id": "p_forward_fold",
        "name": {
            "sanskrit": "Uttanasana",
            "english": "Standing Forward Fold",
            "aliases": ["Standing Forward Bend"]
        },
        "typical_entries": ["p_mountain", "p_upward_salute", "p_halfway_lift"],
        "typical_exits": ["p_halfway_lift", "p_plank", "p_mountain"],
        "pose_intent": [
            "Stretch hamstrings and calves",
            "Release tension in the cervical and lumbar spine",
            "Calm the nervous system (mild inversion)"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion",
            "is_inverted": True,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "glaucoma",
                "action": "avoid",
                "reason": "Head below the heart increases intraocular pressure.",
                "recommended_modification": "halfway_lift"
            },
            {
                "condition": "hypertension",
                "action": "modify_or_avoid",
                "reason": "Inversion can cause a sudden rush of blood to the head.",
                "recommended_modification": "halfway_lift"
            },
            {
                "condition": "herniated_disc",
                "action": "modify",
                "reason": "Spinal flexion under the load of the torso can aggravate discs.",
                "recommended_modification": "knees_deeply_bent"
            }
        ],
        "chronic_pain": [
            {
                "condition": "tight_hamstrings",
                "action": "adjust",
                "reason": "Straight legs force the stretch into the lower back instead of the hamstrings.",
                "recommended_modification": "knees_deeply_bent"
            }
        ],
        "modifications": [
            {
                "name": "Knees Deeply Bent",
                "target_area": "hamstrings",
                "instruction": "Bend your knees as much as needed to let your ribs rest on your thighs."
            },
            {
                "name": "Blocks Under Hands",
                "target_area": "lower_back",
                "instruction": "Place your hands on yoga blocks to bring the floor closer to you."
            }
        ],
        "progression": {
            "beginner": "Deep bend in the knees, hands on shins or blocks.",
            "intermediate": "Legs straighter, fingertips touching the floor.",
            "advanced": "Palms flat on the floor beside feet, chest against thighs."
        },
        "common_mistakes": [
            "Locking the knees",
            "Hinging from the lower back instead of the hips",
            "Holding tension in the neck"
        ],
        "sensory_cues": [
            {"cue": "Let your head hang heavy like a ripe fruit.", "area": "neck"},
            {"cue": "Feel the stretch wrapping around the back of your legs.", "area": "hamstrings"}
        ],
        "drishti": {
            "primary": "tip_of_nose",
            "alternatives": ["navel", "closed_eyes"]
        }
    },
    {
        "client_id": "p_halfway_lift",
        "name": {
            "sanskrit": "Ardha Uttanasana",
            "english": "Halfway Lift",
            "aliases": ["Standing Half Forward Bend"]
        },
        "typical_entries": ["p_forward_fold", "p_downward_dog"],
        "typical_exits": ["p_forward_fold", "p_plank", "p_chaturanga"],
        "pose_intent": [
            "Lengthen the spine",
            "Prepare the back for movement",
            "Stretch the hamstrings safely"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "neck_injury",
                "action": "caution",
                "reason": "Looking up can hyperextend the cervical spine.",
                "recommended_modification": "look_down"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Lifting the torso requires core strength; weakness drops the load into the lower back.",
                "recommended_modification": "hands_on_thighs"
            }
        ],
        "modifications": [
            {
                "name": "Hands on Thighs",
                "target_area": "lower_back",
                "instruction": "Place your hands on your thighs instead of your shins for extra spinal support."
            },
            {
                "name": "Look Down",
                "target_area": "neck",
                "instruction": "Keep your gaze straight down at the floor to maintain a neutral neck."
            }
        ],
        "progression": {
            "beginner": "Hands on thighs, slight bend in knees.",
            "intermediate": "Hands on shins, legs straight.",
            "advanced": "Fingertips on the floor in line with the toes, spine perfectly flat."
        },
        "common_mistakes": [
            "Rounding the upper back",
            "Looking too far forward, straining the neck",
            "Locking the knees"
        ],
        "sensory_cues": [
            {"cue": "Imagine making your back as flat as a table.", "area": "spine"},
            {"cue": "Feel the crown of your head pulling forward away from your tailbone.", "area": "spine"}
        ],
        "drishti": {
            "primary": "floor_slightly_forward",
            "alternatives": ["tip_of_nose"]
        }
    },
    {
        "client_id": "p_warrior_1",
        "name": {
            "sanskrit": "Virabhadrasana I",
            "english": "Warrior 1",
            "aliases": ["Warrior I"]
        },
        "typical_entries": ["p_downward_dog", "p_mountain", "p_low_lunge"],
        "typical_exits": ["p_warrior_2", "p_plank", "p_mountain"],
        "pose_intent": [
            "Strengthen quadriceps, glutes, and ankles",
            "Stretch the hip flexors of the back leg",
            "Open the chest and shoulders"
        ],
        "anatomical_signature": {
            "spinal_shape": "mild_extension",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "hypertension",
                "action": "modify",
                "reason": "Arms overhead combined with large muscle engagement increases cardiac load.",
                "recommended_modification": "hands_at_heart"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Deep lunge places lateral and sheer stress on the front knee.",
                "recommended_modification": "shorten_stance"
            },
            {
                "condition": "ankle_stiffness",
                "action": "modify",
                "reason": "The back foot requires strong dorsiflexion and rotation.",
                "recommended_modification": "high_lunge_heel_up"
            }
        ],
        "modifications": [
            {
                "name": "Shorten Stance",
                "target_area": "knees",
                "instruction": "Step your back foot slightly closer to the front and decrease the bend in your front knee."
            },
            {
                "name": "High Lunge (Heel Up)",
                "target_area": "ankles",
                "instruction": "Lift your back heel off the floor so all toes point forward, relieving ankle pressure."
            }
        ],
        "progression": {
            "beginner": "Short stance, hands on hips.",
            "intermediate": "Deepen the front knee bend to 90 degrees, arms overhead.",
            "advanced": "Palms touching overhead, gaze up, back leg perfectly straight."
        },
        "common_mistakes": [
            "Front knee collapsing inward",
            "Over-arching the lower back",
            "Back foot lifting off the floor"
        ],
        "sensory_cues": [
            {"cue": "Feel your back heel anchoring you down.", "area": "feet"},
            {"cue": "Notice the stretch across the front of your back hip.", "area": "hips"}
        ],
        "drishti": {
            "primary": "thumbs",
            "alternatives": ["straight_ahead"]
        }
    },
    {
        "client_id": "p_warrior_2",
        "name": {
            "sanskrit": "Virabhadrasana II",
            "english": "Warrior 2",
            "aliases": ["Warrior II"]
        },
        "typical_entries": ["p_warrior_1", "p_downward_dog", "p_mountain"],
        "typical_exits": ["p_triangle", "p_extended_side_angle", "p_plank"],
        "pose_intent": [
            "Open the hips and groin",
            "Strengthen the legs and ankles",
            "Build stamina and concentration"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "vertigo",
                "action": "caution",
                "reason": "Turning the head sharply over the front hand can trigger dizziness.",
                "recommended_modification": "neutral_neck"
            }
        ],
        "chronic_pain": [
            {
                "condition": "shoulder_pain",
                "action": "adjust",
                "reason": "Holding arms parallel to the floor fatigues the deltoids and traps.",
                "recommended_modification": "hands_on_hips"
            },
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Front knee flexion combined with external hip rotation can strain the medial collateral ligament (MCL).",
                "recommended_modification": "shorten_stance"
            }
        ],
        "modifications": [
            {
                "name": "Hands on Hips",
                "target_area": "shoulders",
                "instruction": "Rest your hands on your hips to release tension in the shoulders and neck."
            },
            {
                "name": "Neutral Neck",
                "target_area": "neck",
                "instruction": "Keep your chest and gaze facing the side of the room rather than turning your head."
            }
        ],
        "progression": {
            "beginner": "Shorter stance, shallow bend in the front knee.",
            "intermediate": "Front thigh parallel to the floor, arms actively reaching apart.",
            "advanced": "Deepest expression with perfect external rotation of the front hip."
        },
        "common_mistakes": [
            "Leaning the torso over the front leg",
            "Front knee collapsing inward past the big toe",
            "Shrugging the shoulders"
        ],
        "sensory_cues": [
            {"cue": "Imagine your arms are being gently pulled in opposite directions.", "area": "arms"},
            {"cue": "Feel the power and stability in your legs.", "area": "legs"}
        ],
        "drishti": {
            "primary": "front_middle_finger",
            "alternatives": ["side_wall"]
        }
    },
    {
        "client_id": "p_warrior_3",
        "name": {
            "sanskrit": "Virabhadrasana III",
            "english": "Warrior 3",
            "aliases": ["Warrior III", "Flying Warrior"]
        },
        "typical_entries": ["p_high_lunge", "p_warrior_1"],
        "typical_exits": ["p_mountain", "p_high_lunge", "p_standing_split"],
        "pose_intent": [
            "Improve balance and proprioception",
            "Strengthen the standing leg, ankle, and core",
            "Tone the entire posterior chain"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "hypertension",
                "action": "caution",
                "reason": "Intense full-body isometric contraction.",
                "recommended_modification": "airplane_arms"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Lifting the back leg without core engagement hyperextends the lumbar spine.",
                "recommended_modification": "hands_on_blocks"
            },
            {
                "condition": "ankle_stiffness",
                "action": "modify",
                "reason": "Requires immense stability from the standing ankle.",
                "recommended_modification": "wall_support"
            }
        ],
        "modifications": [
            {
                "name": "Hands on Blocks",
                "target_area": "lower_back",
                "instruction": "Place your hands on tall yoga blocks directly under your shoulders for support."
            },
            {
                "name": "Airplane Arms",
                "target_area": "shoulders",
                "instruction": "Reach your arms back alongside your hips like airplane wings."
            }
        ],
        "progression": {
            "beginner": "Hands on blocks or a wall, back leg lifted halfway.",
            "intermediate": "Airplane arms, torso and back leg parallel to the floor.",
            "advanced": "Arms reaching straight forward, biceps by the ears, forming a perfect 'T'."
        },
        "common_mistakes": [
            "Opening the lifted hip toward the ceiling",
            "Locking the standing knee",
            "Dropping the chest below the hips"
        ],
        "sensory_cues": [
            {"cue": "Imagine a straight line of energy from your back heel through the crown of your head.", "area": "full_body"},
            {"cue": "Feel your standing foot gripping the mat for stability.", "area": "feet"}
        ],
        "drishti": {
            "primary": "floor_straight_down",
            "alternatives": ["slightly_forward"]
        }
    },
    {
        "client_id": "p_triangle",
        "name": {
            "sanskrit": "Trikonasana",
            "english": "Triangle Pose",
            "aliases": ["Extended Triangle"]
        },
        "typical_entries": ["p_warrior_2", "p_pyramid"],
        "typical_exits": ["p_warrior_2", "p_half_moon", "p_pyramid"],
        "pose_intent": [
            "Stretch the hamstrings, groin, and hips",
            "Open the chest and shoulders",
            "Strengthen the legs and core"
        ],
        "anatomical_signature": {
            "spinal_shape": "lateral_flexion",
            "is_inverted": False,
            "weight_bearing_points": ["feet", "bottom_hand_optional"]
        },
        "contraindications": [
            {
                "condition": "neck_injury",
                "action": "modify",
                "reason": "Looking up at the top hand strains the cervical spine.",
                "recommended_modification": "look_down"
            }
        ],
        "chronic_pain": [
            {
                "condition": "tight_hamstrings",
                "action": "adjust",
                "reason": "Forcing the hand to the floor rounds the spine and strains the hamstring attachment.",
                "recommended_modification": "hand_on_shin_or_block"
            },
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Hyperextension of the front knee.",
                "recommended_modification": "microbend_front_knee"
            }
        ],
        "modifications": [
            {
                "name": "Hand on Block",
                "target_area": "hamstrings",
                "instruction": "Rest your bottom hand lightly on a block or your shin, never directly on your knee."
            },
            {
                "name": "Look Down",
                "target_area": "neck",
                "instruction": "Keep your gaze down at your front foot to relax your neck."
            }
        ],
        "progression": {
            "beginner": "Hand high on the shin, slight bend in the front knee.",
            "intermediate": "Hand on a block or ankle, top arm reaching straight up.",
            "advanced": "Bottom hand outside the foot on the floor, core holding the torso without dumping weight into the hand."
        },
        "common_mistakes": [
            "Resting the hand directly on the knee joint",
            "Collapsing the top shoulder forward",
            "Hyperextending (locking) the front knee"
        ],
        "sensory_cues": [
            {"cue": "Feel the deep stretch along the side of your body.", "area": "ribs"},
            {"cue": "Imagine leaning back against an invisible wall.", "area": "spine"}
        ],
        "drishti": {
            "primary": "top_thumb",
            "alternatives": ["bottom_foot", "straight_ahead"]
        }
    },
    {
        "client_id": "p_tree",
        "name": {
            "sanskrit": "Vrksasana",
            "english": "Tree Pose",
            "aliases": []
        },
        "typical_entries": ["p_mountain"],
        "typical_exits": ["p_mountain", "p_warrior_3"],
        "pose_intent": [
            "Improve balance and focus",
            "Strengthen the standing leg and ankle",
            "Externally rotate and open the hip"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["feet"]
        },
        "contraindications": [
            {
                "condition": "vertigo",
                "action": "modify",
                "reason": "Standing on one leg challenges the vestibular system.",
                "recommended_modification": "kickstand_foot"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "avoid_specific_placement",
                "reason": "Pressing the foot directly against the inner knee joint forces it laterally out of alignment.",
                "recommended_modification": "foot_below_knee"
            }
        ],
        "modifications": [
            {
                "name": "Kickstand",
                "target_area": "balance",
                "instruction": "Keep your toes on the floor and rest your heel against your inner ankle."
            },
            {
                "name": "Foot Below Knee",
                "target_area": "knees",
                "instruction": "Place your foot flat against your inner calf, completely avoiding the knee joint."
            }
        ],
        "progression": {
            "beginner": "Kickstand variation, hands at the heart.",
            "intermediate": "Foot on the inner calf or thigh, arms growing overhead.",
            "advanced": "Foot high on the inner thigh, gaze lifted or eyes closed."
        },
        "common_mistakes": [
            "Placing the foot directly on the knee joint",
            "Sinking the hip of the standing leg out to the side",
            "Holding the breath while balancing"
        ],
        "sensory_cues": [
            {"cue": "Press your foot into your leg, and your leg equally back into your foot.", "area": "legs"},
            {"cue": "Feel yourself rooted to the floor, yet growing taller through your spine.", "area": "spine"}
        ],
        "drishti": {
            "primary": "steady_point_forward",
            "alternatives": ["upward"]
        }
    },{
        "client_id": "p_cat",
        "name": {
            "sanskrit": "Marjaryasana",
            "english": "Cat Pose",
            "aliases": ["Cat Stretch"]
        },
        "typical_entries": ["p_table_top", "p_cow"],
        "typical_exits": ["p_cow", "p_childs_pose", "p_downward_dog"],
        "pose_intent": [
            "Stretch the posterior torso and neck",
            "Provide a gentle massage to the spine and belly organs",
            "Release tension in the cervical and thoracic spine"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion",
            "is_inverted": False,
            "weight_bearing_points": ["palms", "knees", "shins"]
        },
        "contraindications": [
            {
                "condition": "neck_injury",
                "action": "modify",
                "reason": "Dropping the head completely can strain injured cervical discs.",
                "recommended_modification": "neutral_neck_cat"
            }
        ],
        "chronic_pain": [
            {
                "condition": "wrist_pain",
                "action": "modify",
                "reason": "Weight-bearing in full extension compresses the wrists.",
                "recommended_modification": "fists_or_forearms"
            },
            {
                "condition": "knee_pain",
                "action": "modify",
                "reason": "Direct pressure on the patella against the floor.",
                "recommended_modification": "padded_knees"
            }
        ],
        "modifications": [
            {
                "name": "Neutral Neck Cat",
                "target_area": "neck",
                "instruction": "Keep your gaze between your hands rather than tucking your chin to your chest."
            },
            {
                "name": "Fists or Forearms",
                "target_area": "wrists",
                "instruction": "Make fists with your hands or drop to your forearms to relieve wrist compression."
            },
            {
                "name": "Padded Knees",
                "target_area": "knees",
                "instruction": "Place a folded blanket directly under your knees for cushioning."
            }
        ],
        "progression": {
            "beginner": "Focus on moving the middle back toward the ceiling.",
            "intermediate": "Coordinate the movement perfectly with the exhale.",
            "advanced": "Engage the pelvic floor (Mula Bandha) deeply at the peak of the flexion."
        },
        "common_mistakes": [
            "Forcing the chin too hard into the chest",
            "Shrugging the shoulders up toward the ears",
            "Locking the elbows"
        ],
        "sensory_cues": [
            {"cue": "Imagine a string pulling the center of your back up toward the ceiling.", "area": "spine"},
            {"cue": "Feel your shoulder blades spreading wide apart.", "area": "upper_back"}
        ],
        "drishti": {
            "primary": "navel",
            "alternatives": ["closed_eyes"]
        }
    },
    {
        "client_id": "p_cow",
        "name": {
            "sanskrit": "Bitilasana",
            "english": "Cow Pose",
            "aliases": ["Cow Stretch"]
        },
        "typical_entries": ["p_table_top", "p_cat"],
        "typical_exits": ["p_cat", "p_downward_dog", "p_childs_pose"],
        "pose_intent": [
            "Stretch the front torso and neck",
            "Open the chest to encourage deeper breathing",
            "Mobilize the lumbar and cervical spine"
        ],
        "anatomical_signature": {
            "spinal_shape": "extension",
            "is_inverted": False,
            "weight_bearing_points": ["palms", "knees", "shins"]
        },
        "contraindications": [
            {
                "condition": "neck_injury",
                "action": "modify",
                "reason": "Looking up sharply compresses the cervical vertebrae.",
                "recommended_modification": "look_forward"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Dumping weight into the lower back causes painful facet joint compression.",
                "recommended_modification": "engage_core"
            },
            {
                "condition": "wrist_pain",
                "action": "modify",
                "reason": "Weight-bearing in extension compresses wrists.",
                "recommended_modification": "fists_or_forearms"
            }
        ],
        "modifications": [
            {
                "name": "Look Forward",
                "target_area": "neck",
                "instruction": "Keep your gaze straight ahead rather than craning your neck to look up."
            },
            {
                "name": "Engage Core",
                "target_area": "lower_back",
                "instruction": "Keep a slight lifting action in your belly to support your lower back as it arches."
            }
        ],
        "progression": {
            "beginner": "Focus on dropping the belly gently without forcing.",
            "intermediate": "Broaden the collarbones and pull the heart forward through the arms.",
            "advanced": "Isolate the movement, allowing the spine to ripple sequentially from tailbone to crown."
        },
        "common_mistakes": [
            "Collapsing heavily into the lower back without core support",
            "Cranking the neck upward",
            "Bending the elbows"
        ],
        "sensory_cues": [
            {"cue": "Feel your collarbones widening like a smile.", "area": "chest"},
            {"cue": "Imagine your heart melting forward between your biceps.", "area": "chest"}
        ],
        "drishti": {
            "primary": "third_eye",
            "alternatives": ["straight_ahead", "tip_of_nose"]
        }
    },
    {
        "client_id": "p_downward_dog",
        "name": {
            "sanskrit": "Adho Mukha Svanasana",
            "english": "Downward Facing Dog",
            "aliases": ["Down Dog", "Inverted V"]
        },
        "typical_entries": ["p_plank", "p_table_top", "p_cow"],
        "typical_exits": ["p_plank", "p_forward_fold", "p_low_lunge", "p_childs_pose"],
        "pose_intent": [
            "Lengthen the spine",
            "Stretch the posterior chain (hamstrings, calves)",
            "Strengthen shoulders and arms"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": True,
            "weight_bearing_points": ["palms", "feet"]
        },
        "contraindications": [
            {"condition": "hypertension", "action": "modify_or_avoid", "reason": "Inversion may increase blood pressure.", "recommended_modification": "puppy_pose"},
            {"condition": "glaucoma", "action": "avoid", "reason": "Increases intraocular pressure.", "recommended_modification": None},
            {"condition": "vertigo", "action": "modify", "reason": "Change in head position causes dizziness.", "recommended_modification": "puppy_pose"}
        ],
        "chronic_pain": [
            {"condition": "wrist_pain", "action": "modify", "reason": "Weight-bearing compresses the wrist joint.", "recommended_modification": "dolphin_pose"},
            {"condition": "tight_hamstrings", "action": "adjust", "reason": "Limited flexibility strains the back.", "recommended_modification": "bend_knees"}
        ],
        "modifications": [
            {"name": "Dolphin Pose", "target_area": "wrists", "instruction": "Lower your forearms to the mat, pressing firmly through the forearms to lift hips."},
            {"name": "Puppy Pose", "target_area": "cardiovascular", "instruction": "Bring your knees to the mat, walk hands forward, and lower your chest, keeping head above heart."},
            {"name": "Bend Knees", "target_area": "hamstrings", "instruction": "Bend your knees deeply while keeping your spine long and hips lifting up."}
        ],
        "progression": {
            "beginner": "Keep knees bent and focus on lengthening the spine.",
            "intermediate": "Work toward straightening the legs while maintaining spinal length.",
            "advanced": "Fully extend the legs with stable shoulders and grounded heels."
        },
        "common_mistakes": [
            "Rounding the back",
            "Dumping weight into the wrists",
            "Forcing heels to the floor"
        ],
        "sensory_cues": [
            {"cue": "Feel the length growing from your hands to your hips.", "area": "spine"},
            {"cue": "Imagine your heels gently melting toward the mat.", "area": "legs"}
        ],
        "drishti": {
            "primary": "navel",
            "alternatives": ["between_feet"]
        }
    },
    {
        "client_id": "p_childs_pose",
        "name": {
            "sanskrit": "Balasana",
            "english": "Child's Pose",
            "aliases": ["Resting Pose"]
        },
        "typical_entries": ["p_table_top", "p_downward_dog", "p_hero_pose"],
        "typical_exits": ["p_table_top", "p_downward_dog", "p_cobra"],
        "pose_intent": [
            "Release tension in the lower back",
            "Gently stretch hips and thighs",
            "Calm the mind and regulate breath"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion",
            "is_inverted": False,
            "weight_bearing_points": ["shins", "forehead", "forearms"]
        },
        "contraindications": [
            {
                "condition": "pregnancy",
                "action": "modify",
                "reason": "Compression of the abdomen.",
                "recommended_modification": "wide_knee_childs_pose"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "modify",
                "reason": "Deep flexion compresses the meniscus.",
                "recommended_modification": "blanket_under_knees_or_hips"
            },
            {
                "condition": "ankle_stiffness",
                "action": "modify",
                "reason": "Deep plantar flexion stretches the anterior ankle tightly.",
                "recommended_modification": "rolled_blanket_under_ankles"
            }
        ],
        "modifications": [
            {
                "name": "Wide Knee Childs Pose",
                "target_area": "hips",
                "instruction": "Take your knees as wide as the mat to create space for your belly and chest."
            },
            {
                "name": "Blanket Support",
                "target_area": "knees",
                "instruction": "Place a rolled blanket between your calves and hamstrings to reduce knee flexion."
            }
        ],
        "progression": {
            "beginner": "Use a bolster under the torso for full support.",
            "intermediate": "Knees wide, arms actively reaching forward.",
            "advanced": "Knees together, arms back, breath directed fully into the posterior ribcage."
        },
        "common_mistakes": [
            "Forcing hips to heels causing knee pain",
            "Holding tension in the shoulders"
        ],
        "sensory_cues": [
            {"cue": "Feel your hips sinking heavier toward your heels with every exhale.", "area": "hips"},
            {"cue": "Notice the solid support of the earth beneath your forehead.", "area": "head"}
        ],
        "drishti": {
            "primary": "closed_eyes",
            "alternatives": ["inward"]
        }
    },
    {
        "client_id": "p_plank",
        "name": {
            "sanskrit": "Phalakasana",
            "english": "Plank Pose",
            "aliases": ["High Plank", "Upper Push-up"]
        },
        "typical_entries": ["p_downward_dog", "p_forward_fold", "p_table_top"],
        "typical_exits": ["p_chaturanga", "p_downward_dog", "p_childs_pose"],
        "pose_intent": [
            "Build core, shoulder, and arm strength",
            "Create full-body isometric tension",
            "Prepare for arm balances and transitions"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["palms", "toes"]
        },
        "contraindications": [
            {
                "condition": "hypertension",
                "action": "caution",
                "reason": "Intense isometric holds can cause temporary blood pressure spikes if breath is held.",
                "recommended_modification": "knees_down_plank"
            }
        ],
        "chronic_pain": [
            {
                "condition": "wrist_pain",
                "action": "modify",
                "reason": "Full body weight is loaded onto wrists in 90-degree extension.",
                "recommended_modification": "forearm_plank"
            },
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "If the core weakens, the lower back arches and takes the load.",
                "recommended_modification": "knees_down_plank"
            }
        ],
        "modifications": [
            {
                "name": "Forearm Plank",
                "target_area": "wrists",
                "instruction": "Lower down to your forearms, keeping your elbows directly beneath your shoulders."
            },
            {
                "name": "Knees Down Plank",
                "target_area": "lower_back",
                "instruction": "Gently drop your knees to the mat, maintaining a straight line from your head to your knees."
            }
        ],
        "progression": {
            "beginner": "Knees on the mat, focusing on pressing the floor away.",
            "intermediate": "Full high plank, heels pressing back, core braced.",
            "advanced": "Shift weight slightly forward onto the tiptoes in preparation for Chaturanga."
        },
        "common_mistakes": [
            "Dropping the hips and sagging the lower back",
            "Piking the hips up too high",
            "Collapsing between the shoulder blades"
        ],
        "sensory_cues": [
            {"cue": "Feel your belly button pulling up toward your spine.", "area": "core"},
            {"cue": "Imagine pushing the floor away to fill the space between your shoulder blades.", "area": "upper_back"}
        ],
        "drishti": {
            "primary": "top_of_mat",
            "alternatives": ["slightly_forward"]
        }
    },
    {
        "client_id": "p_cobra",
        "name": {
            "sanskrit": "Bhujangasana",
            "english": "Cobra Pose",
            "aliases": ["Baby Cobra"]
        },
        "typical_entries": ["p_prone_savasana", "p_chaturanga"],
        "typical_exits": ["p_downward_dog", "p_childs_pose", "p_prone_savasana"],
        "pose_intent": [
            "Strengthen the spinal erectors",
            "Open the chest and shoulders",
            "Counteract forward-hunching posture"
        ],
        "anatomical_signature": {
            "spinal_shape": "extension",
            "is_inverted": False,
            "weight_bearing_points": ["pelvis", "tops_of_feet", "palms (lightly)"]
        },
        "contraindications": [
            {
                "condition": "pregnancy",
                "action": "avoid",
                "reason": "Direct pressure on the abdomen is unsafe.",
                "recommended_modification": "cow_pose"
            },
            {
                "condition": "herniated_disc",
                "action": "modify_or_avoid",
                "reason": "Spinal extension can compress affected posterior discs.",
                "recommended_modification": "sphinx_pose"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Pushing up too high jams the lumbar facet joints.",
                "recommended_modification": "baby_cobra"
            }
        ],
        "modifications": [
            {
                "name": "Baby Cobra",
                "target_area": "lower_back",
                "instruction": "Lift only your chest off the mat using your back muscles, keeping little to no weight in your hands."
            },
            {
                "name": "Sphinx Pose",
                "target_area": "lower_back",
                "instruction": "Slide your forearms forward and rest on your elbows to reduce the arch in your back."
            }
        ],
        "progression": {
            "beginner": "Baby cobra, hands hovering off the mat.",
            "intermediate": "Palms lightly pressing, lifting higher while keeping the pubis grounded.",
            "advanced": "Full expression with elbows slightly bent, chest pulling actively forward."
        },
        "common_mistakes": [
            "Using arm strength to push up instead of back strength",
            "Crunching the back of the neck by looking too far up",
            "Letting the elbows splay out to the sides"
        ],
        "sensory_cues": [
            {"cue": "Feel the front of your chest peeling away from the earth.", "area": "chest"},
            {"cue": "Imagine your shoulder blades sliding down toward your back pockets.", "area": "shoulders"}
        ],
        "drishti": {
            "primary": "straight_ahead",
            "alternatives": ["tip_of_nose"]
        }
    },
    {
        "client_id": "p_sphinx",
        "name": {
            "sanskrit": "Salamba Bhujangasana",
            "english": "Sphinx Pose",
            "aliases": ["Supported Cobra"]
        },
        "typical_entries": ["p_prone_savasana", "p_cobra"],
        "typical_exits": ["p_prone_savasana", "p_childs_pose", "p_seal_pose"],
        "pose_intent": [
            "Provide a gentle, supported backbend",
            "Open the chest and lungs safely",
            "Alleviate lower back fatigue"
        ],
        "anatomical_signature": {
            "spinal_shape": "mild_extension",
            "is_inverted": False,
            "weight_bearing_points": ["forearms", "pelvis", "tops_of_feet"]
        },
        "contraindications": [
            {
                "condition": "pregnancy",
                "action": "avoid",
                "reason": "Direct pressure on the abdomen is unsafe.",
                "recommended_modification": "cow_pose"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "If glutes and core relax completely, the lower back takes all the compression.",
                "recommended_modification": "slide_elbows_forward"
            }
        ],
        "modifications": [
            {
                "name": "Slide Elbows Forward",
                "target_area": "lower_back",
                "instruction": "Walk your elbows slightly ahead of your shoulders to decrease the intensity of the backbend."
            }
        ],
        "progression": {
            "beginner": "Elbows slightly forward, focusing on deep breathing.",
            "intermediate": "Elbows directly under shoulders, actively dragging forearms back to pull chest forward.",
            "advanced": "Transition into Seal Pose by straightening the arms."
        },
        "common_mistakes": [
            "Sinking the chest between the shoulders",
            "Clenching the glutes too tightly",
            "Looking too far upward"
        ],
        "sensory_cues": [
            {"cue": "Feel the gentle traction as you energetically pull your elbows toward your hips.", "area": "spine"},
            {"cue": "Notice the quiet, steady opening across your collarbones.", "area": "chest"}
        ],
        "drishti": {
            "primary": "straight_ahead",
            "alternatives": ["closed_eyes"]
        }
    },
    {
        "client_id": "p_upward_dog",
        "name": {
            "sanskrit": "Urdhva Mukha Svanasana",
            "english": "Upward Facing Dog",
            "aliases": ["Up Dog"]
        },
        "typical_entries": ["p_chaturanga"],
        "typical_exits": ["p_downward_dog", "p_childs_pose"],
        "pose_intent": [
            "Deeply stretch the anterior chain (chest, abdomen, hip flexors)",
            "Strengthen the wrists, arms, and spine",
            "Stimulate abdominal organs"
        ],
        "anatomical_signature": {
            "spinal_shape": "extension",
            "is_inverted": False,
            "weight_bearing_points": ["palms", "tops_of_feet"]
        },
        "contraindications": [
            {
                "condition": "pregnancy",
                "action": "avoid",
                "reason": "Overstretches the abdomen and compresses the lumbar spine.",
                "recommended_modification": "cow_pose"
            },
            {
                "condition": "herniated_disc",
                "action": "avoid",
                "reason": "Intense spinal extension can severely aggravate disc issues.",
                "recommended_modification": "sphinx_pose"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "modify",
                "reason": "Hanging in the joints causes severe lower back compression.",
                "recommended_modification": "cobra_pose"
            },
            {
                "condition": "wrist_pain",
                "action": "modify",
                "reason": "Bears significant body weight in deep wrist extension.",
                "recommended_modification": "sphinx_pose"
            }
        ],
        "modifications": [
            {
                "name": "Cobra Pose",
                "target_area": "lower_back",
                "instruction": "Keep your thighs and pelvis on the floor and maintain a slight bend in your elbows."
            }
        ],
        "progression": {
            "beginner": "Substitute with Cobra Pose.",
            "intermediate": "Lift thighs off the mat, pressing firmly through the tops of the feet.",
            "advanced": "Full extension with thighs lifted, chest pulling fiercely through the upper arms."
        },
        "common_mistakes": [
            "Letting the thighs rest on the floor (which turns it into a poorly aligned Cobra)",
            "Hanging the head back completely, crunching the neck",
            "Shoulders creeping up to the ears"
        ],
        "sensory_cues": [
            {"cue": "Imagine your heart shining brightly forward like a headlight.", "area": "chest"},
            {"cue": "Feel the tops of your feet pressing down so firmly that your kneecaps lift.", "area": "legs"}
        ],
        "drishti": {
            "primary": "tip_of_nose",
            "alternatives": ["slightly_upward"]
        }
    },
    {
        "client_id": "p_easy_pose",
        "name": {
            "sanskrit": "Sukhasana",
            "english": "Easy Pose",
            "aliases": ["Cross-legged Seat"]
        },
        "typical_entries": ["p_staff_pose", "p_standing_forward_fold"],
        "typical_exits": ["p_seated_forward_fold", "p_table_top", "p_staff_pose"],
        "pose_intent": [
            "Promote groundedness and mental clarity",
            "Open the hips and stretch the knees and ankles",
            "Provide a steady seat for meditation and pranayama"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["sit_bones", "outer_ankles"]
        },
        "contraindications": [
            {
                "condition": "sciatica",
                "action": "caution",
                "reason": "Sitting flat can compress the sciatic nerve.",
                "recommended_modification": "sit_on_block"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Deep flexion and external rotation strain the medial knee ligaments.",
                "recommended_modification": "blocks_under_knees"
            },
            {
                "condition": "hip_tightness",
                "action": "adjust",
                "reason": "Tight hips cause the lower back to round backward.",
                "recommended_modification": "sit_on_cushion"
            }
        ],
        "modifications": [
            {
                "name": "Elevated Seat",
                "target_area": "hips",
                "instruction": "Sit on the edge of a folded blanket or block to elevate your hips above your knees."
            },
            {
                "name": "Blocks Under Knees",
                "target_area": "knees",
                "instruction": "Place blocks or pillows under your knees so they can rest without hanging in the air."
            }
        ],
        "progression": {
            "beginner": "Sit on a bolster, legs loosely crossed.",
            "intermediate": "Sit flat on the floor, shins crossed, maintaining a long spine.",
            "advanced": "Hold for extended meditation without fidgeting or losing spinal integrity."
        },
        "common_mistakes": [
            "Slumping the lower back",
            "Jutting the chin forward (tech neck)",
            "Forcing the knees toward the floor"
        ],
        "sensory_cues": [
            {"cue": "Feel your sit bones heavy and rooted into the prop beneath you.", "area": "pelvis"},
            {"cue": "Let your shoulders melt down away from your ears.", "area": "shoulders"}
        ],
        "drishti": {
            "primary": "closed_eyes",
            "alternatives": ["third_eye"]
        }
    },
    {
        "client_id": "p_staff_pose",
        "name": {
            "sanskrit": "Dandasana",
            "english": "Staff Pose",
            "aliases": ["Seated Staff"]
        },
        "typical_entries": ["p_downward_dog", "p_easy_pose"],
        "typical_exits": ["p_seated_forward_fold", "p_head_to_knee", "p_easy_pose"],
        "pose_intent": [
            "Improve postural awareness",
            "Strengthen back muscles and core",
            "Stretch the hamstrings and calves"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["sit_bones", "heels", "palms (lightly)"]
        },
        "contraindications": [
            {
                "condition": "sciatica",
                "action": "caution",
                "reason": "90-degree hip flexion with straight legs stretches the sciatic nerve aggressively.",
                "recommended_modification": "bend_knees"
            }
        ],
        "chronic_pain": [
            {
                "condition": "tight_hamstrings",
                "action": "adjust",
                "reason": "Pulls the pelvis backward, rounding the lower spine.",
                "recommended_modification": "sit_on_blanket"
            },
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "Requires significant core strength to sit upright; weakness causes lumbar strain.",
                "recommended_modification": "wall_support"
            }
        ],
        "modifications": [
            {
                "name": "Sit on Blanket",
                "target_area": "hamstrings",
                "instruction": "Sit on a folded blanket to tilt your pelvis forward and relieve the hamstrings."
            },
            {
                "name": "Wall Support",
                "target_area": "lower_back",
                "instruction": "Sit with your back pressed flat against a wall to help support your spine."
            }
        ],
        "progression": {
            "beginner": "Sit on a blanket, knees slightly bent.",
            "intermediate": "Sit flat, legs straight, heels pressing away.",
            "advanced": "Perfect 90-degree angle, hands hovering off the floor, fully supported by the core."
        },
        "common_mistakes": [
            "Leaning backward on the hands",
            "Rounding the upper back",
            "Letting the feet splay open"
        ],
        "sensory_cues": [
            {"cue": "Imagine your torso and legs forming a perfect right angle.", "area": "full_body"},
            {"cue": "Feel the crown of your head reaching up as your tailbone roots down.", "area": "spine"}
        ],
        "drishti": {
            "primary": "toes",
            "alternatives": ["straight_ahead"]
        }
    },
    {
        "client_id": "p_seated_forward_fold",
        "name": {
            "sanskrit": "Paschimottanasana",
            "english": "Seated Forward Bend",
            "aliases": ["Seated Forward Fold"]
        },
        "typical_entries": ["p_staff_pose"],
        "typical_exits": ["p_staff_pose", "p_bridge_pose", "p_head_to_knee"],
        "pose_intent": [
            "Deeply stretch the entire posterior chain (hamstrings, calves, spine)",
            "Calm the nervous system",
            "Stimulate abdominal organs"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion",
            "is_inverted": False,
            "weight_bearing_points": ["sit_bones", "heels", "calves"]
        },
        "contraindications": [
            {
                "condition": "herniated_disc",
                "action": "avoid",
                "reason": "Intense seated spinal flexion forces disc material backward.",
                "recommended_modification": "staff_pose"
            },
            {
                "condition": "pregnancy",
                "action": "modify",
                "reason": "Compresses the abdomen.",
                "recommended_modification": "wide_leg_forward_fold"
            }
        ],
        "chronic_pain": [
            {
                "condition": "tight_hamstrings",
                "action": "adjust",
                "reason": "Causes extreme pulling on the lower back if legs remain straight.",
                "recommended_modification": "use_strap"
            }
        ],
        "modifications": [
            {
                "name": "Use a Strap",
                "target_area": "hamstrings",
                "instruction": "Loop a strap around your feet and hold the ends to keep your spine long as you gently pull."
            },
            {
                "name": "Microbend Knees",
                "target_area": "lower_back",
                "instruction": "Keep a generous bend in your knees, prioritizing a straight back over straight legs."
            }
        ],
        "progression": {
            "beginner": "Use a strap, knees bent, spine straight.",
            "intermediate": "Hold the outer edges of the feet, chest reaching toward the toes.",
            "advanced": "Forehead resting comfortably on the shins, elbows resting on the floor."
        },
        "common_mistakes": [
            "Rounding the upper back to force the head down",
            "Pulling aggressively with the arms",
            "Locking the knees"
        ],
        "sensory_cues": [
            {"cue": "Think about pulling your heart toward your toes rather than your nose to your knees.", "area": "chest"},
            {"cue": "Feel a deep, calming release traveling up the back of your legs.", "area": "hamstrings"}
        ],
        "drishti": {
            "primary": "toes",
            "alternatives": ["shins", "closed_eyes"]
        }
    },
    {
        "client_id": "p_head_to_knee",
        "name": {
            "sanskrit": "Janu Sirsasana",
            "english": "Head-to-Knee Forward Bend",
            "aliases": ["Seated Head to Knee"]
        },
        "typical_entries": ["p_staff_pose", "p_seated_forward_fold"],
        "typical_exits": ["p_seated_forward_fold", "p_easy_pose", "p_staff_pose"],
        "pose_intent": [
            "Stretch the hamstrings, spine, and groins",
            "Calm the brain and help relieve mild depression",
            "Stimulate the liver and kidneys"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion_with_mild_rotation",
            "is_inverted": False,
            "weight_bearing_points": ["sit_bones", "extended_leg_heel", "bent_knee_outer_edge"]
        },
        "contraindications": [
            {
                "condition": "herniated_disc",
                "action": "avoid",
                "reason": "The combination of spinal flexion and mild rotation is highly stressful on lumbar discs.",
                "recommended_modification": "staff_pose"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "modify",
                "reason": "Deep flexion and external rotation of the bent knee stresses the medial meniscus.",
                "recommended_modification": "block_under_bent_knee"
            },
            {
                "condition": "tight_hamstrings",
                "action": "adjust",
                "reason": "Pulls the pelvis into posterior tilt, rounding the lower back excessively.",
                "recommended_modification": "use_strap"
            }
        ],
        "modifications": [
            {
                "name": "Block Under Bent Knee",
                "target_area": "knees",
                "instruction": "Place a block or folded blanket beneath your bent knee so it has solid support and doesn't hang in the air."
            },
            {
                "name": "Use a Strap",
                "target_area": "hamstrings",
                "instruction": "Loop a strap around the foot of your extended leg to keep your spine long as you fold."
            }
        ],
        "progression": {
            "beginner": "Sit on a folded blanket, use a strap, keep spine completely straight.",
            "intermediate": "Hold the foot, bending elbows out to the sides, lowering the chest toward the thigh.",
            "advanced": "Rest forehead on the shin, clasp wrists beyond the extended foot."
        },
        "common_mistakes": [
            "Rounding the upper back to force the head down",
            "Letting the extended leg roll outward",
            "Collapsing the chest over the bent knee instead of the straight leg"
        ],
        "sensory_cues": [
            {"cue": "Imagine aiming your heart toward your toes, keeping the front of your body long.", "area": "chest"},
            {"cue": "Feel a gentle, twisting release in your lower back on the side of the bent knee.", "area": "lower_back"}
        ],
        "drishti": {
            "primary": "toes",
            "alternatives": ["closed_eyes"]
        }
    },
    {
        "client_id": "p_pigeon",
        "name": {
            "sanskrit": "Eka Pada Rajakapotasana",
            "english": "Pigeon Pose",
            "aliases": ["Half Pigeon", "Sleeping Pigeon"]
        },
        "typical_entries": ["p_downward_dog", "p_table_top", "p_low_lunge"],
        "typical_exits": ["p_downward_dog", "p_table_top", "p_seated_forward_fold"],
        "pose_intent": [
            "Deeply stretch the hip rotators (gluteus, piriformis) of the front leg",
            "Stretch the hip flexors (psoas) of the back leg",
            "Release emotional and physical tension stored in the pelvis"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral_to_mild_extension",
            "is_inverted": False,
            "weight_bearing_points": ["front_shin", "back_knee", "top_of_back_foot", "forearms_if_folded"]
        },
        "contraindications": [
            {
                "condition": "recent_surgery",
                "action": "avoid",
                "reason": "Hip replacements or recent knee surgeries cannot tolerate extreme external rotation.",
                "recommended_modification": "supine_figure_four"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "avoid",
                "reason": "Intense lateral torque is placed on the front knee if the hip lacks mobility.",
                "recommended_modification": "supine_figure_four"
            },
            {
                "condition": "hip_tightness",
                "action": "modify",
                "reason": "Causes the practitioner to roll completely onto one side, misaligning the spine.",
                "recommended_modification": "prop_under_hip"
            }
        ],
        "modifications": [
            {
                "name": "Supine Figure Four",
                "target_area": "knees",
                "instruction": "Lie on your back, cross your right ankle over your left thigh, and pull your left knee toward your chest. This protects the knee completely."
            },
            {
                "name": "Prop Under Hip",
                "target_area": "hips",
                "instruction": "Place a blanket or block under the hip of your bent leg to keep your pelvis level with the floor."
            }
        ],
        "progression": {
            "beginner": "Keep the front heel close to the groin, stay lifted on the hands.",
            "intermediate": "Walk hands forward and lower down to the forearms.",
            "advanced": "Rest forehead on the floor, arms extended forward, front shin parallel to the top of the mat."
        },
        "common_mistakes": [
            "Rolling onto the outer hip of the bent leg",
            "Forcing the front shin parallel to the mat, causing knee torque",
            "Tensing the shoulders while folding forward"
        ],
        "sensory_cues": [
            {"cue": "Send your breath directly into the tightness of your outer hip.", "area": "hips"},
            {"cue": "With every exhale, imagine sinking a millimeter deeper into the mat.", "area": "full_body"}
        ],
        "drishti": {
            "primary": "closed_eyes",
            "alternatives": ["floor_straight_down"]
        }
    },
    {
        "client_id": "p_bridge",
        "name": {
            "sanskrit": "Setu Bandhasana",
            "english": "Bridge Pose",
            "aliases": ["Two-Legged Inverted Staff"]
        },
        "typical_entries": ["p_corpse_pose", "p_knees_to_chest"],
        "typical_exits": ["p_corpse_pose", "p_happy_baby", "p_knees_to_chest"],
        "pose_intent": [
            "Open the chest, heart, and shoulders",
            "Strengthen the glutes, hamstrings, and erector spinae",
            "Prepare the spine for deeper backbends or inversions"
        ],
        "anatomical_signature": {
            "spinal_shape": "extension",
            "is_inverted": True,
            "weight_bearing_points": ["shoulders", "back_of_head", "feet"]
        },
        "contraindications": [
            {
                "condition": "neck_injury",
                "action": "caution",
                "reason": "Bears weight on the cervical spine while in flexion.",
                "recommended_modification": "supported_bridge_low_block"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "modify",
                "reason": "Over-clenching the glutes or weak hamstrings can jam the lumbar spine.",
                "recommended_modification": "supported_bridge"
            },
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Feet placed too far or too close to hips places shear force on knees.",
                "recommended_modification": "adjust_foot_distance"
            }
        ],
        "modifications": [
            {
                "name": "Supported Bridge",
                "target_area": "lower_back",
                "instruction": "Slide a yoga block under your sacrum (the hard bone at the base of your spine) and rest your weight completely on it."
            },
            {
                "name": "Adjust Foot Distance",
                "target_area": "knees",
                "instruction": "Walk your feet forward or backward until your shins are perfectly vertical when your hips are lifted."
            }
        ],
        "progression": {
            "beginner": "Dynamic bridge: lifting hips on the inhale, lowering on the exhale.",
            "intermediate": "Hold the lift, interlace hands underneath the back, roll onto the tops of the shoulders.",
            "advanced": "Transition into full Wheel Pose (Urdhva Dhanurasana)."
        },
        "common_mistakes": [
            "Turning the head side to side (dangerous for the neck)",
            "Letting the knees splay outward",
            "Over-clenching the glutes instead of using the hamstrings"
        ],
        "sensory_cues": [
            {"cue": "Feel your shins pulling slightly backward toward your shoulders to engage your hamstrings.", "area": "legs"},
            {"cue": "Notice the spaciousness expanding across your collarbones.", "area": "chest"}
        ],
        "drishti": {
            "primary": "straight_up",
            "alternatives": ["heart_center", "closed_eyes"]
        }
    },
    {
        "client_id": "p_happy_baby",
        "name": {
            "sanskrit": "Ananda Balasana",
            "english": "Happy Baby Pose",
            "aliases": ["Dead Bug Pose"]
        },
        "typical_entries": ["p_knees_to_chest", "p_bridge"],
        "typical_exits": ["p_corpse_pose", "p_knees_to_chest", "p_supine_twist"],
        "pose_intent": [
            "Gently stretch the inner groins and back spine",
            "Release the lower back and sacrum",
            "Calm the mind and relieve stress"
        ],
        "anatomical_signature": {
            "spinal_shape": "mild_flexion",
            "is_inverted": False,
            "weight_bearing_points": ["entire_back", "sacrum", "back_of_head"]
        },
        "contraindications": [
            {
                "condition": "pregnancy",
                "action": "modify_or_avoid",
                "reason": "Lying flat on the back in later stages compresses the vena cava.",
                "recommended_modification": "seated_bound_angle"
            }
        ],
        "chronic_pain": [
            {
                "condition": "knee_pain",
                "action": "adjust",
                "reason": "Pulling down on the feet can torque the knee if hips are tight.",
                "recommended_modification": "hold_behind_knees"
            },
            {
                "condition": "lower_back_pain",
                "action": "adjust",
                "reason": "If the tailbone lifts completely off the floor, it strains the lumbar spine.",
                "recommended_modification": "tailbone_down"
            }
        ],
        "modifications": [
            {
                "name": "Hold Behind Knees",
                "target_area": "knees",
                "instruction": "Instead of grabbing your feet, wrap your hands behind your thighs to safely pull your knees wide."
            },
            {
                "name": "Tailbone Down",
                "target_area": "lower_back",
                "instruction": "Focus on pressing your tailbone flat into the mat, even if it means you can't pull your knees as low."
            }
        ],
        "progression": {
            "beginner": "Hold the backs of the thighs, tailbone rooted.",
            "intermediate": "Hold the outer edges of the feet, ankles stacked directly over knees.",
            "advanced": "Gently rock side to side, massaging the spine against the floor."
        },
        "common_mistakes": [
            "Lifting the tailbone and lower back off the floor",
            "Lifting the head and shoulders up to reach the feet",
            "Feet dropping down toward the glutes instead of pointing at the ceiling"
        ],
        "sensory_cues": [
            {"cue": "Let your tailbone grow heavy, anchoring you to the earth.", "area": "lower_back"},
            {"cue": "Feel the gentle, broad opening across your inner thighs.", "area": "hips"}
        ],
        "drishti": {
            "primary": "closed_eyes",
            "alternatives": ["straight_up"]
        }
    },
    {
        "client_id": "p_shoulder_stand",
        "name": {
            "sanskrit": "Salamba Sarvangasana",
            "english": "Supported Shoulder Stand",
            "aliases": ["Shoulderstand", "Queen of Poses"]
        },
        "typical_entries": ["p_bridge", "p_halasana"],
        "typical_exits": ["p_halasana", "p_corpse_pose", "p_fish_pose"],
        "pose_intent": [
            "Improve venous blood return from the legs",
            "Stimulate the thyroid and parathyroid glands",
            "Calm the central nervous system deeply"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion",
            "is_inverted": True,
            "weight_bearing_points": ["shoulders", "back_of_head", "elbows"]
        },
        "contraindications": [
            {"condition": "glaucoma", "action": "avoid", "reason": "Massive increase in intraocular pressure.", "recommended_modification": None},
            {"condition": "hypertension", "action": "avoid", "reason": "Forces a large volume of blood toward the heart and brain under compression.", "recommended_modification": "legs_up_the_wall"},
            {"condition": "neck_injury", "action": "avoid", "reason": "Extreme cervical flexion bearing body weight.", "recommended_modification": "legs_up_the_wall"},
            {"condition": "pregnancy", "action": "modify_or_avoid", "reason": "Risk of falling and abdominal compression.", "recommended_modification": "legs_up_the_wall"}
        ],
        "chronic_pain": [
            {
                "condition": "neck_pain",
                "action": "avoid",
                "reason": "Flattening the cervical curve under load can herniate discs.",
                "recommended_modification": "legs_up_the_wall"
            }
        ],
        "modifications": [
            {
                "name": "Legs Up The Wall",
                "target_area": "neck",
                "instruction": "Scoot your hips against a wall and extend your legs straight up it, keeping your back perfectly flat on the floor."
            },
            {
                "name": "Blanket Support",
                "target_area": "neck",
                "instruction": "Place neatly folded blankets under your shoulders so your head rests on the floor, preserving the natural curve of your neck."
            }
        ],
        "progression": {
            "beginner": "Legs Up The Wall or a block under the sacrum with legs in the air.",
            "intermediate": "Use blanket support, hands supporting the mid-back, legs angled slightly back.",
            "advanced": "Perfectly vertical alignment from shoulders to toes, hands resting near the shoulder blades."
        },
        "common_mistakes": [
            "Turning the head while in the pose (can cause severe injury)",
            "Splaying the elbows too wide, losing structural support",
            "Dumping weight into the neck instead of pressing through the shoulders"
        ],
        "sensory_cues": [
            {"cue": "Keep your gaze locked strictly upward—protecting your neck is paramount.", "area": "neck"},
            {"cue": "Imagine the blood flowing out of your feet, cascading gently down your legs to cool your heart.", "area": "legs"}
        ],
        "drishti": {
            "primary": "toes",
            "alternatives": ["chest"]
        }
    },
    {
        "client_id": "p_halasana",
        "name": {
            "sanskrit": "Halasana",
            "english": "Plow Pose",
            "aliases": ["Plough Pose"]
        },
        "typical_entries": ["p_shoulder_stand", "p_bridge"],
        "typical_exits": ["p_corpse_pose", "p_happy_baby", "p_shoulder_stand"],
        "pose_intent": [
            "Deeply stretch the cervical and thoracic spine",
            "Stimulate the abdominal organs and thyroid",
            "Prepare the body for final relaxation"
        ],
        "anatomical_signature": {
            "spinal_shape": "flexion",
            "is_inverted": True,
            "weight_bearing_points": ["shoulders", "back_of_head", "toes"]
        },
        "contraindications": [
            {"condition": "glaucoma", "action": "avoid", "reason": "Severe increase in intraocular pressure.", "recommended_modification": None},
            {"condition": "hypertension", "action": "avoid", "reason": "Blood flow forced toward the head under compression.", "recommended_modification": "legs_up_the_wall"},
            {"condition": "neck_injury", "action": "avoid", "reason": "Extreme cervical flexion under load.", "recommended_modification": "seated_forward_fold"}
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "caution",
                "reason": "Deep spinal flexion can aggravate lumbar discs.",
                "recommended_modification": "supported_bridge"
            }
        ],
        "modifications": [
            {
                "name": "Feet on Chair",
                "target_area": "hamstrings",
                "instruction": "If your feet don't reach the floor easily, rest your toes on a chair or bolster placed behind your head."
            },
            {
                "name": "Legs Up The Wall",
                "target_area": "neck",
                "instruction": "Skip the neck compression entirely and simply rest your legs up a wall."
            }
        ],
        "progression": {
            "beginner": "Avoid full pose. Practice Legs Up The Wall.",
            "intermediate": "Support the lower back with hands, toes resting on a prop.",
            "advanced": "Toes tucked on the floor behind the head, arms interlaced and pressing into the mat."
        },
        "common_mistakes": [
            "Turning the head from side to side",
            "Forcing the feet to the floor, compromising the neck",
            "Collapsing the chest into the chin, restricting the airway"
        ],
        "sensory_cues": [
            {"cue": "Keep your gaze straight up; imagine a hollow space between your neck and the floor.", "area": "neck"},
            {"cue": "Feel the deep, quiet stretch traveling down the entire length of your spine.", "area": "spine"}
        ],
        "drishti": {
            "primary": "navel",
            "alternatives": ["straight_up", "closed_eyes"]
        }
    },
    {
        "client_id": "p_corpse_pose",
        "name": {
            "sanskrit": "Savasana",
            "english": "Corpse Pose",
            "aliases": ["Final Relaxation"]
        },
        "typical_entries": ["p_happy_baby", "p_supine_twist", "p_halasana"],
        "typical_exits": ["p_easy_pose", "session_end"],
        "pose_intent": [
            "Integrate the physical and energetic benefits of the practice",
            "Lower the heart rate and blood pressure",
            "Transition into a state of deep meditation and rest"
        ],
        "anatomical_signature": {
            "spinal_shape": "neutral",
            "is_inverted": False,
            "weight_bearing_points": ["back_of_head", "shoulders", "sacrum", "calves", "heels"]
        },
        "contraindications": [
            {
                "condition": "pregnancy",
                "action": "modify",
                "reason": "Lying flat in late stages restricts blood flow in the inferior vena cava.",
                "recommended_modification": "side_lying_savasana"
            }
        ],
        "chronic_pain": [
            {
                "condition": "lower_back_pain",
                "action": "modify",
                "reason": "Lying flat can cause the lumbar spine to arch due to tight hip flexors (psoas pull).",
                "recommended_modification": "bolster_under_knees"
            }
        ],
        "modifications": [
            {
                "name": "Bolster Under Knees",
                "target_area": "lower_back",
                "instruction": "Place a rolled blanket or bolster beneath your knees to allow your lower back to flatten and release."
            },
            {
                "name": "Side-Lying Savasana",
                "target_area": "cardiovascular",
                "instruction": "Lie on your left side with a pillow between your knees for comfort."
            }
        ],
        "progression": {
            "beginner": "Use props for physical comfort.",
            "intermediate": "Lie flat, focusing on sequential muscle relaxation.",
            "advanced": "Achieve complete stillness of body and mind for 10+ minutes without falling asleep."
        },
        "common_mistakes": [
            "Fidgeting or adjusting clothing",
            "Keeping the teeth clenched or the tongue pressed against the roof of the mouth",
            "Skipping the pose entirely"
        ],
        "sensory_cues": [
            {"cue": "Feel your body becoming so heavy it begins to sink into the floor.", "area": "full_body"},
            {"cue": "Let your breath become natural, soft, and completely effortless.", "area": "breath"},
            {"cue": "Notice the space between your eyebrows softening and widening.", "area": "face"}
        ],
        "drishti": {
            "primary": "closed_eyes",
            "alternatives": ["inward_focus"]
        }
    }
]

async def seed_database():
    """
    Connects to MongoDB using Motor (async) and upserts the yoga postures.
    Upsert ensures idempotent execution.
    """

    # --- MONGODB CONFIGURATION ---
    MONGO_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "yoga"
    COLLECTION_NAME = "postures"

    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    try:
        # Verify connection
        await client.admin.command('ping')
        print(f"✅ Successfully connected to MongoDB at {MONGO_URI}")
        
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]
        
        # Prepare bulk operations
        operations = [
            UpdateOne(
                {"client_id": posture["client_id"]},
                {"$set": posture},
                upsert=True
            )
            for posture in postures_data
        ]
        
        if operations:
            result = await collection.bulk_write(operations)
            print(f"✅ Database Seeding Complete!")
            print(f"   - Documents inserted/upserted: {result.upserted_count}")
            print(f"   - Documents modified: {result.modified_count}")
            print(f"   - Total postures processed: {len(postures_data)}")
            print("\nNote: Request the next batch of postures to continue populating the database.")
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())