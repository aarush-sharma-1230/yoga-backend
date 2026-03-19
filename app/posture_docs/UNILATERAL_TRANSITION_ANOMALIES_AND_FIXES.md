# Unilateral Pose Transition Anomalies & Fixes

This document lists all anomalies found in `typical_entries` and `typical_exits` for unilateral poses, where transitions incorrectly included both left and right variants when only one side is anatomically possible. Each fix ensures that side-specific poses only transition to poses that match the same side (or to the opposite side explicitly when switching sides).

---

## 1. Warrior 1 (Left Leg Forward) — `p_warrior_1_left`

**Anomaly:** `typical_exits` included `p_warrior_2_right`. From Warrior 1 with left leg forward, opening the hip leads only to Warrior 2 with left leg forward, not right.

**Rule:** Warrior 1 → Warrior 2 is a same-side transition (open the front hip). You cannot go from left-leg-forward to right-leg-forward without switching.

**Fix Applied:**
- **typical_exits:** Removed `p_warrior_2_right`. Kept only `p_warrior_2_left`, `p_plank`, `p_mountain`, `p_warrior_1_right` (switch sides).

---

## 2. Warrior 1 (Right Leg Forward) — `p_warrior_1_right`

**Anomaly:** `typical_exits` included `p_warrior_2_left`. From Warrior 1 with right leg forward, opening the hip leads only to Warrior 2 with right leg forward.

**Rule:** Same as above — same-side transition only.

**Fix Applied:**
- **typical_exits:** Removed `p_warrior_2_left`. Kept only `p_warrior_2_right`, `p_plank`, `p_mountain`, `p_warrior_1_left` (switch sides).

---

## 3. Warrior 2 (Left Leg Forward) — `p_warrior_2_left`

**Anomaly:** `typical_exits` included `p_triangle_right`. From Warrior 2 with left leg forward, you bend toward the front leg to enter Triangle. That front leg is the left, so you can only reach Triangle (left leg forward).

**Rule:** Warrior 2 → Triangle is a same-side transition. You bend toward the leg that is already forward.

**Fix Applied:**
- **typical_exits:** Removed `p_triangle_right`. Kept only `p_triangle_left`, `p_extended_side_angle`, `p_plank`, `p_warrior_2_right` (switch sides).

---

## 4. Warrior 2 (Right Leg Forward) — `p_warrior_2_right`

**Anomaly:** `typical_exits` included `p_triangle_left`. Same reasoning as above — bending toward the right front leg leads only to Triangle (right leg forward).

**Fix Applied:**
- **typical_exits:** Removed `p_triangle_left`. Kept only `p_triangle_right`, `p_extended_side_angle`, `p_plank`, `p_warrior_2_left` (switch sides).

---

## 5. Warrior 3 (Left Leg Forward) — `p_warrior_3_left`

**Anomaly:** `typical_entries` included `p_warrior_1_right` and `p_tree_right`. Warrior 3 left means left leg is the standing leg. You can only arrive there from:
- Warrior 1 left (lift the right/back leg) → Warrior 3 left
- Tree left (left leg lifted, standing on right) → step forward → left leg becomes standing = Warrior 3 left

You cannot get Warrior 3 left from Warrior 1 right or Tree right.

**Rule:** Warrior 3 inherits the “front” leg from the previous pose. Tree (left leg lifted) → Warrior 3 (left leg forward). Warrior 1 (left leg forward) → Warrior 3 (left leg forward).

**Fix Applied:**
- **typical_entries:** Removed `p_warrior_1_right`, `p_tree_right`. Kept only `p_high_lunge`, `p_warrior_1_left`, `p_tree_left`.

---

## 6. Warrior 3 (Right Leg Forward) — `p_warrior_3_right`

**Anomaly:** `typical_entries` included `p_warrior_1_left` and `p_tree_left`. Same reasoning — you can only reach Warrior 3 right from Warrior 1 right or Tree right.

**Fix Applied:**
- **typical_entries:** Removed `p_warrior_1_left`, `p_tree_left`. Kept only `p_high_lunge`, `p_warrior_1_right`, `p_tree_right`.

---

## 7. Triangle Pose (Left Leg Forward) — `p_triangle_left`

**Anomaly (entries):** `typical_entries` included `p_warrior_2_right`. You reach Triangle left only by bending from Warrior 2 left (left leg forward). Warrior 2 right cannot lead to Triangle left without a full side switch.

**Anomaly (exits):** `typical_exits` included `p_warrior_2_right`. From Triangle left, coming back up returns you to Warrior 2 left. You do not land in Warrior 2 right.

**Rule:** Triangle and Warrior 2 share the same front leg. Entries and exits are same-side only (plus switch-side transitions like `p_triangle_right`).

**Fix Applied:**
- **typical_entries:** Removed `p_warrior_2_right`. Kept only `p_warrior_2_left`, `p_pyramid`.
- **typical_exits:** Removed `p_warrior_2_right`. Kept only `p_warrior_2_left`, `p_half_moon`, `p_pyramid`, `p_triangle_right` (switch sides).

---

## 8. Triangle Pose (Right Leg Forward) — `p_triangle_right`

**Anomaly (entries):** `typical_entries` included `p_warrior_2_left`. Triangle right is only reached from Warrior 2 right.

**Anomaly (exits):** `typical_exits` included `p_warrior_2_left`. From Triangle right, you return to Warrior 2 right only.

**Fix Applied:**
- **typical_entries:** Removed `p_warrior_2_left`. Kept only `p_warrior_2_right`, `p_pyramid`.
- **typical_exits:** Removed `p_warrior_2_left`. Kept only `p_warrior_2_right`, `p_half_moon`, `p_pyramid`, `p_triangle_left` (switch sides).

---

## 9. Tree Pose (Left Leg Lifted) — `p_tree_left`

**Anomaly:** `typical_exits` included `p_warrior_3_right`. In Tree left, the left leg is lifted and the right leg is standing. Stepping forward, you place the left foot down, so the left leg becomes the standing leg → Warrior 3 left. You cannot go from Tree left to Warrior 3 right without changing which leg was lifted.

**Rule:** Tree (X leg lifted) → Warrior 3 (X leg forward). The lifted leg becomes the standing leg when you step forward.

**Fix Applied:**
- **typical_exits:** Removed `p_warrior_3_right`. Kept only `p_mountain`, `p_warrior_3_left`, `p_tree_right` (switch legs).

---

## 10. Tree Pose (Right Leg Lifted) — `p_tree_right`

**Anomaly:** `typical_exits` included `p_warrior_3_left`. Same reasoning — Tree right (right leg lifted) → step forward → Warrior 3 right only.

**Fix Applied:**
- **typical_exits:** Removed `p_warrior_3_left`. Kept only `p_mountain`, `p_warrior_3_right`, `p_tree_left` (switch legs).

---

## Poses Verified as Correct (No Changes Needed)

### Head-to-Knee Forward Bend (Left/Right)
- **Entries:** Staff pose and Seated forward fold can lead to either side (practitioner chooses which leg to bend). ✓
- **Exits:** Each side can transition to the opposite side (switch), or to seated forward fold, easy pose, staff pose. ✓

### Pigeon Pose (Left/Right)
- **Entries:** Downward dog and Table top can lead to either side (practitioner chooses which leg to bring forward). ✓
- **Exits:** Each side can transition to the opposite side (switch), or to downward dog, table top. ✓

### Mountain Pose
- **Exits:** Can lead to Tree left OR Tree right (practitioner chooses which leg to lift). ✓

### Downward Dog
- **Exits:** Can lead to Warrior 1 left/right and Pigeon left/right (practitioner chooses which leg to step through). ✓

### Table Top
- **Exits:** Can lead to Pigeon left or Pigeon right (practitioner chooses which leg to extend back). ✓

---

## Summary Table

| Pose | Field | Anomaly | Fix |
|------|-------|---------|-----|
| p_warrior_1_left | typical_exits | Had p_warrior_2_right | Removed; keep only p_warrior_2_left (same side) |
| p_warrior_1_right | typical_exits | Had p_warrior_2_left | Removed; keep only p_warrior_2_right (same side) |
| p_warrior_2_left | typical_exits | Had p_triangle_right | Removed; keep only p_triangle_left (same side) |
| p_warrior_2_right | typical_exits | Had p_triangle_left | Removed; keep only p_triangle_right (same side) |
| p_warrior_3_left | typical_entries | Had p_warrior_1_right, p_tree_right | Removed; keep only p_warrior_1_left, p_tree_left |
| p_warrior_3_right | typical_entries | Had p_warrior_1_left, p_tree_left | Removed; keep only p_warrior_1_right, p_tree_right |
| p_triangle_left | typical_entries | Had p_warrior_2_right | Removed; keep only p_warrior_2_left |
| p_triangle_left | typical_exits | Had p_warrior_2_right | Removed; keep only p_warrior_2_left |
| p_triangle_right | typical_entries | Had p_warrior_2_left | Removed; keep only p_warrior_2_right |
| p_triangle_right | typical_exits | Had p_warrior_2_left | Removed; keep only p_warrior_2_right |
| p_tree_left | typical_exits | Had p_warrior_3_right | Removed; keep only p_warrior_3_left |
| p_tree_right | typical_exits | Had p_warrior_3_left | Removed; keep only p_warrior_3_right |
