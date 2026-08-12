package com.wahidvr.kamera

import android.graphics.*
import kotlin.math.*
import kotlin.random.Random

class EffectManager {

    data class Effect(
        val id: String,
        val name: String,
        val category: String,
        val color: Int
    )

    val effects = listOf(
        // ==================== KATEGORI 1: Transformasi AI ====================
        Effect("ai_mini_me", "AI Mini Me", "Transformasi AI", Color.parseColor("#FF69B4")),
        Effect("ai_giant", "AI Giant", "Transformasi AI", Color.parseColor("#FF4500")),
        Effect("ghibli", "Ghibli Style", "Transformasi AI", Color.parseColor("#98FB98")),
        Effect("pixar", "Pixar Style", "Transformasi AI", Color.parseColor("#87CEEB")),
        Effect("anime", "Anime Style", "Transformasi AI", Color.parseColor("#FFB6C1")),
        Effect("cyberpunk", "Cyberpunk", "Transformasi AI", Color.parseColor("#00FFFF")),
        Effect("superhero", "Superhero", "Transformasi AI", Color.parseColor("#FF0000")),
        Effect("robot", "Robot", "Transformasi AI", Color.parseColor("#808080")),
        Effect("alien", "Alien", "Transformasi AI", Color.parseColor("#00FF00")),
        Effect("old_to_young", "Old to Young", "Transformasi AI", Color.parseColor("#DEB887")),
        Effect("young_to_old", "Young to Old", "Transformasi AI", Color.parseColor("#D2691E")),
        Effect("beauty_ai", "Beauty AI", "Transformasi AI", Color.parseColor("#FFB6C1")),
        Effect("avatar_anime", "Avatar Anime", "Transformasi AI", Color.parseColor("#FF69B4")),
        Effect("avatar_cartoon", "Avatar Cartoon", "Transformasi AI", Color.parseColor("#FFA500")),

        // ==================== KATEGORI 2: Face AI ====================
        Effect("face_tracking", "Face Tracking", "Face AI", Color.parseColor("#00D4FF")),
        Effect("head_tracking", "Head Tracking", "Face AI", Color.parseColor("#0088CC")),
        Effect("eye_glow", "Eye Glow", "Face AI", Color.parseColor("#FF00FF")),
        Effect("laser_eyes", "Laser Eyes", "Face AI", Color.parseColor("#FF0000")),
        Effect("floating_head", "Floating Head", "Face AI", Color.parseColor("#8A2BE2")),
        Effect("clone_effect", "Clone Effect", "Face AI", Color.parseColor("#00CED1")),
        Effect("invisible_body", "Invisible Body", "Face AI", Color.parseColor("#4169E1")),
        Effect("body_freeze", "Body Freeze", "Face AI", Color.parseColor("#00FFFF")),
        Effect("morph_face", "Morph Face", "Face AI", Color.parseColor("#FF1493")),
        Effect("smile_enhancement", "Smile Enhancement", "Face AI", Color.parseColor("#FFD700")),
        Effect("face_scan", "Face Scan", "Face AI", Color.parseColor("#00FF00")),
        Effect("emotion_happy", "Emotion Happy", "Face AI", Color.parseColor("#FFD700")),
        Effect("emotion_sad", "Emotion Sad", "Face AI", Color.parseColor("#4169E1")),
        Effect("emotion_surprised", "Emotion Surprised", "Face AI", Color.parseColor("#FF4500")),
        Effect("emotion_angry", "Emotion Angry", "Face AI", Color.parseColor("#DC143C")),
        Effect("galaxy_eyes", "Galaxy Eyes", "Face AI", Color.parseColor("#9400D3")),

        // ==================== KATEGORI 3: VR Portal ====================
        Effect("vr_portal", "VR Portal", "VR Portal", Color.parseColor("#9400D3")),
        Effect("teleport_portal", "Teleport Portal", "VR Portal", Color.parseColor("#00FFFF")),
        Effect("mirror_dimension", "Mirror Dimension", "VR Portal", Color.parseColor("#C0C0C0")),
        Effect("multiverse_portal", "Multiverse Portal", "VR Portal", Color.parseColor("#FF00FF")),
        Effect("wormhole_jump", "Wormhole Jump", "VR Portal", Color.parseColor("#4B0082")),
        Effect("quantum_tunnel", "Quantum Tunnel", "VR Portal", Color.parseColor("#00BFFF")),
        Effect("time_portal", "Time Portal", "VR Portal", Color.parseColor("#FFD700")),
        Effect("black_hole_portal", "Black Hole Portal", "VR Portal", Color.parseColor("#000000")),
        Effect("door_another_world", "Door Another World", "VR Portal", Color.parseColor("#8B4513")),
        Effect("infinite_room", "Infinite Room", "VR Portal", Color.parseColor("#DDA0DD")),
        Effect("galaxy_portal", "Galaxy Portal", "VR Portal", Color.parseColor("#4B0082")),
        Effect("fire_portal", "Fire Portal", "VR Portal", Color.parseColor("#FF4500")),
        Effect("ice_portal", "Ice Portal", "VR Portal", Color.parseColor("#00FFFF")),
        Effect("water_portal", "Water Portal", "VR Portal", Color.parseColor("#0000CD")),
        Effect("lightning_portal", "Lightning Portal", "VR Portal", Color.parseColor("#FFFF00")),
        Effect("cloud_portal", "Cloud Portal", "VR Portal", Color.parseColor("#F5F5F5")),
        Effect("crystal_portal", "Crystal Portal", "VR Portal", Color.parseColor("#E0FFFF")),
        Effect("ancient_portal", "Ancient Portal", "VR Portal", Color.parseColor("#8B4513")),
        Effect("fantasy_gate", "Fantasy Gate", "VR Portal", Color.parseColor("#9932CC")),

        // ==================== KATEGORI 4: VR Vision ====================
        Effect("360_equirectangular", "360 Equirectangular", "VR Vision", Color.parseColor("#00D4FF")),
        Effect("little_planet", "Little Planet", "VR Vision", Color.parseColor("#228B22")),
        Effect("tiny_planet_spin", "Tiny Planet Spin", "VR Vision", Color.parseColor("#32CD32")),
        Effect("fisheye_ultra", "Fisheye Ultra", "VR Vision", Color.parseColor("#00CED1")),
        Effect("super_fisheye", "Super Fisheye", "VR Vision", Color.parseColor("#20B2AA")),
        Effect("barrel_distortion", "Barrel Distortion", "VR Vision", Color.parseColor("#48D1CC")),
        Effect("ultra_wide", "Ultra Wide", "VR Vision", Color.parseColor("#008B8B")),
        Effect("macro_vr", "Macro VR", "VR Vision", Color.parseColor("#00FA9A")),
        Effect("telephoto_compression", "Telephoto Compression", "VR Vision", Color.parseColor("#66CDAA")),
        Effect("panoramic_stitch", "Panoramic Stitch", "VR Vision", Color.parseColor("#8FBC8F")),
        Effect("spherical_lens", "Spherical Lens", "VR Vision", Color.parseColor("#3CB371")),
        Effect("dome_lens", "Dome Lens", "VR Vision", Color.parseColor("#2E8B57")),
        Effect("curved_lens", "Curved Lens", "VR Vision", Color.parseColor("#006400")),
        Effect("anamorphic_vr", "Anamorphic VR", "VR Vision", Color.parseColor("#556B2F")),
        Effect("tilt_shift_vr", "Tilt Shift VR", "VR Vision", Color.parseColor("#6B8E23")),
        Effect("lens_flare_vr", "Lens Flare VR", "VR Vision", Color.parseColor("#FFD700")),
        Effect("prism_lens", "Prism Lens", "VR Vision", Color.parseColor("#FF69B4")),
        Effect("kaleidoscope_lens", "Kaleidoscope Lens", "VR Vision", Color.parseColor("#FF1493")),
        Effect("crystal_lens", "Crystal Lens", "VR Vision", Color.parseColor("#E0FFFF")),
        Effect("glass_refraction", "Glass Refraction", "VR Vision", Color.parseColor("#ADD8E6")),

        // ==================== KATEGORI 5: VR 360 View ====================
        Effect("360_street_view", "360 Street View", "VR 360 View", Color.parseColor("#808080")),
        Effect("360_drone_view", "360 Drone View", "VR 360 View", Color.parseColor("#87CEEB")),
        Effect("360_rooftop_view", "360 Rooftop View", "VR 360 View", Color.parseColor("#B0C4DE")),
        Effect("360_stadium_view", "360 Stadium View", "VR 360 View", Color.parseColor("#228B22")),
        Effect("360_concert_view", "360 Concert View", "VR 360 View", Color.parseColor("#FF1493")),
        Effect("360_classroom_view", "360 Classroom View", "VR 360 View", Color.parseColor("#DEB887")),
        Effect("360_museum_view", "360 Museum View", "VR 360 View", Color.parseColor("#DAA520")),
        Effect("360_city_view", "360 City View", "VR 360 View", Color.parseColor("#708090")),
        Effect("360_forest_view", "360 Forest View", "VR 360 View", Color.parseColor("#228B22")),
        Effect("360_beach_view", "360 Beach View", "VR 360 View", Color.parseColor("#F4A460")),
        Effect("360_mountain_view", "360 Mountain View", "VR 360 View", Color.parseColor("#696969")),
        Effect("360_space_view", "360 Space View", "VR 360 View", Color.parseColor("#191970")),
        Effect("360_underwater_view", "360 Underwater View", "VR 360 View", Color.parseColor("#0000CD")),
        Effect("360_night_view", "360 Night View", "VR 360 View", Color.parseColor("#191970")),
        Effect("360_time_freeze", "360 Time Freeze", "VR 360 View", Color.parseColor("#00FFFF")),
        Effect("360_mirror_world", "360 Mirror World", "VR 360 View", Color.parseColor("#C0C0C0")),
        Effect("360_infinite_room", "360 Infinite Room", "VR 360 View", Color.parseColor("#DDA0DD")),
        Effect("360_portal_room", "360 Portal Room", "VR 360 View", Color.parseColor("#9400D3")),
        Effect("360_floating_island", "360 Floating Island", "VR 360 View", Color.parseColor("#87CEEB")),
        Effect("360_miniature_world", "360 Miniature World", "VR 360 View", Color.parseColor("#98FB98")),

        // ==================== KATEGORI 6: VR Mirror ====================
        Effect("mirror_portal", "Mirror Portal", "VR Mirror", Color.parseColor("#C0C0C0")),
        Effect("mirror_clone_viral", "Mirror Clone Viral", "VR Mirror", Color.parseColor("#FFD700")),
        Effect("infinite_mirror_viral", "Infinite Mirror Viral", "VR Mirror", Color.parseColor("#E6E6FA")),
        Effect("reflection_world", "Reflection World", "VR Mirror", Color.parseColor("#B0E0E6")),
        Effect("mirror_dimension_v", "Mirror Dimension", "VR Mirror", Color.parseColor("#C0C0C0")),
        Effect("mirror_explosion", "Mirror Explosion", "VR Mirror", Color.parseColor("#FF4500")),
        Effect("mirror_maze", "Mirror Maze", "VR Mirror", Color.parseColor("#DDA0DD")),
        Effect("infinite_reflection", "Infinite Reflection", "VR Mirror", Color.parseColor("#F5F5F5")),
        Effect("reverse_reflection", "Reverse Reflection", "VR Mirror", Color.parseColor("#AFEEEE")),
        Effect("broken_mirror_world", "Broken Mirror World", "VR Mirror", Color.parseColor("#808080")),
        Effect("liquid_mirror", "Liquid Mirror", "VR Mirror", Color.parseColor("#00BFFF")),
        Effect("galaxy_mirror", "Galaxy Mirror", "VR Mirror", Color.parseColor("#4B0082")),
        Effect("cyber_mirror", "Cyber Mirror", "VR Mirror", Color.parseColor("#00FFFF")),

        // ==================== KATEGORI 7: VR Teleport Through ====================
        Effect("teleport_behind_camera", "Teleport Behind Camera", "VR Teleport", Color.parseColor("#9400D3")),
        Effect("teleport_through_phone", "Teleport Through Phone", "VR Teleport", Color.parseColor("#00D4FF")),
        Effect("teleport_through_screen", "Teleport Through Screen", "VR Teleport", Color.parseColor("#0088CC")),
        Effect("teleport_through_glass", "Teleport Through Glass", "VR Teleport", Color.parseColor("#ADD8E6")),
        Effect("teleport_through_shadow", "Teleport Through Shadow", "VR Teleport", Color.parseColor("#2F4F4F")),
        Effect("teleport_through_water", "Teleport Through Water", "VR Teleport", Color.parseColor("#0000CD")),
        Effect("teleport_through_fire", "Teleport Through Fire", "VR Teleport", Color.parseColor("#FF4500")),
        Effect("teleport_through_lightning", "Teleport Through Lightning", "VR Teleport", Color.parseColor("#FFFF00")),
        Effect("teleport_through_clouds", "Teleport Through Clouds", "VR Teleport", Color.parseColor("#F5F5F5")),
        Effect("teleport_into_space", "Teleport Into Space", "VR Teleport", Color.parseColor("#191970")),

        // ==================== KATEGORI 8: VR Comes Alive ====================
        Effect("object_comes_alive", "Object Comes Alive", "VR Comes Alive", Color.parseColor("#FF69B4")),
        Effect("photo_comes_alive", "Photo Comes Alive", "VR Comes Alive", Color.parseColor("#FFA500")),
        Effect("painting_comes_alive", "Painting Comes Alive", "VR Comes Alive", Color.parseColor("#DEB887")),
        Effect("statue_comes_alive", "Statue Comes Alive", "VR Comes Alive", Color.parseColor("#808080")),
        Effect("poster_comes_alive", "Poster Comes Alive", "VR Comes Alive", Color.parseColor("#FF4500")),
        Effect("logo_comes_alive", "Logo Comes Alive", "VR Comes Alive", Color.parseColor("#FFD700")),
        Effect("text_comes_alive", "Text Comes Alive", "VR Comes Alive", Color.parseColor("#00FF00")),
        Effect("drawing_comes_alive", "Drawing Comes Alive", "VR Comes Alive", Color.parseColor("#FF1493")),
        Effect("shadow_comes_alive", "Shadow Comes Alive", "VR Comes Alive", Color.parseColor("#2F4F4F")),
        Effect("reflection_comes_alive", "Reflection Comes Alive", "VR Comes Alive", Color.parseColor("#C0C0C0")),

        // ==================== KATEGORI 9: VR Body Transform ====================
        Effect("body_becomes_smoke", "Body Becomes Smoke", "VR Body Transform", Color.parseColor("#808080")),
        Effect("body_becomes_water", "Body Becomes Water", "VR Body Transform", Color.parseColor("#0000CD")),
        Effect("body_becomes_fire", "Body Becomes Fire", "VR Body Transform", Color.parseColor("#FF4500")),
        Effect("body_becomes_ice", "Body Becomes Ice", "VR Body Transform", Color.parseColor("#00FFFF")),
        Effect("body_becomes_glass", "Body Becomes Glass", "VR Body Transform", Color.parseColor("#ADD8E6")),
        Effect("body_becomes_crystal", "Body Becomes Crystal", "VR Body Transform", Color.parseColor("#E0FFFF")),
        Effect("body_becomes_metal", "Body Becomes Metal", "VR Body Transform", Color.parseColor("#A9A9A9")),
        Effect("body_becomes_gold", "Body Becomes Gold", "VR Body Transform", Color.parseColor("#FFD700")),
        Effect("body_becomes_stone", "Body Becomes Stone", "VR Body Transform", Color.parseColor("#696969")),
        Effect("body_becomes_sand", "Body Becomes Sand", "VR Body Transform", Color.parseColor("#F4A460")),
        Effect("ai_melt", "AI Melt", "VR Body Transform", Color.parseColor("#FF69B4")),
        Effect("ai_squish", "AI Squish", "VR Body Transform", Color.parseColor("#FF1493")),
        Effect("cakeify", "Cakeify", "VR Body Transform", Color.parseColor("#DEB887")),
        Effect("glass_break", "Glass Break", "VR Body Transform", Color.parseColor("#ADD8E6")),
        Effect("ice_freeze", "Ice Freeze", "VR Body Transform", Color.parseColor("#00FFFF")),
        Effect("liquid_metal", "Liquid Metal", "VR Body Transform", Color.parseColor("#C0C0C0")),
        Effect("crystal", "Crystal", "VR Body Transform", Color.parseColor("#E0FFFF")),
        Effect("gold", "Gold", "VR Body Transform", Color.parseColor("#FFD700")),
        Effect("smoke_dissolve", "Smoke Dissolve", "VR Body Transform", Color.parseColor("#808080")),
        Effect("pixel_disintegration", "Pixel Disintegration", "VR Body Transform", Color.parseColor("#00FF00")),

        // ==================== KATEGORI 10: VR Face FX ====================
        Effect("face_morph", "Face Morph", "VR Face FX", Color.parseColor("#FF1493")),
        Effect("face_pixel_morph", "Face Pixel Morph", "VR Face FX", Color.parseColor("#00FF00")),
        Effect("face_hologram", "Face Hologram", "VR Face FX", Color.parseColor("#00FFFF")),
        Effect("face_crystal", "Face Crystal", "VR Face FX", Color.parseColor("#E0FFFF")),
        Effect("face_galaxy", "Face Galaxy", "VR Face FX", Color.parseColor("#4B0082")),
        Effect("face_liquid", "Face Liquid", "VR Face FX", Color.parseColor("#00BFFF")),
        Effect("face_robot", "Face Robot", "VR Face FX", Color.parseColor("#808080")),
        Effect("face_anime_v", "Face Anime", "VR Face FX", Color.parseColor("#FFB6C1")),
        Effect("face_digital_scan", "Face Digital Scan", "VR Face FX", Color.parseColor("#00FF00")),
        Effect("face_particle_explosion", "Face Particle Explosion", "VR Face FX", Color.parseColor("#FF4500")),
        Effect("face_scan", "Face Scan", "VR Face FX", Color.parseColor("#00D4FF")),
        Effect("royal_filter", "Royal Filter", "VR Face FX", Color.parseColor("#FFD700")),
        Effect("cyberpunk_hud", "Cyberpunk HUD", "VR Face FX", Color.parseColor("#00FFFF")),

        // ==================== KATEGORI 11: VR Environment Transform ====================
        Effect("city_transform", "City Transform", "VR Environment", Color.parseColor("#708090")),
        Effect("room_transform", "Room Transform", "VR Environment", Color.parseColor("#DEB887")),
        Effect("day_to_night", "Day to Night", "VR Environment", Color.parseColor("#191970")),
        Effect("night_to_day", "Night to Day", "VR Environment", Color.parseColor("#FFD700")),
        Effect("earth_to_space", "Earth to Space", "VR Environment", Color.parseColor("#000080")),
        Effect("street_to_cyberpunk", "Street to Cyberpunk", "VR Environment", Color.parseColor("#00FFFF")),
        Effect("real_to_anime", "Real to Anime", "VR Environment", Color.parseColor("#FFB6C1")),
        Effect("real_to_game", "Real to Game", "VR Environment", Color.parseColor("#00FF00")),
        Effect("real_to_fantasy", "Real to Fantasy", "VR Environment", Color.parseColor("#9932CC")),
        Effect("real_to_metaverse", "Real to Metaverse", "VR Environment", Color.parseColor("#FF00FF")),
        Effect("ocean_appears", "Ocean Appears", "VR Environment", Color.parseColor("#0000CD")),
        Effect("forest_appears", "Forest Appears", "VR Environment", Color.parseColor("#228B22")),
        Effect("street_transforms", "Street Transforms", "VR Environment", Color.parseColor("#808080")),
        Effect("house_transforms", "House Transforms", "VR Environment", Color.parseColor("#DEB887")),
        Effect("building_transforms", "Building Transforms", "VR Environment", Color.parseColor("#708090")),
        Effect("school_transforms", "School Transforms", "VR Environment", Color.parseColor("#B8860B")),
        Effect("mall_transforms", "Mall Transforms", "VR Environment", Color.parseColor("#DDA0DD")),
        Effect("office_transforms", "Office Transforms", "VR Environment", Color.parseColor("#A9A9A9")),
        Effect("room_transforms_v", "Room Transforms", "VR Environment", Color.parseColor("#DEB887")),
        Effect("car_transforms", "Car Transforms", "VR Environment", Color.parseColor("#C0C0C0")),
        Effect("landscape_transforms", "Landscape Transforms", "VR Environment", Color.parseColor("#228B22")),
        Effect("entire_city_transforms", "Entire City Transforms", "VR Environment", Color.parseColor("#708090")),

        // ==================== KATEGORI 12: VR Sky ====================
        Effect("sky_opens", "Sky Opens", "VR Sky", Color.parseColor("#87CEEB")),
        Effect("sky_portal_v", "Sky Portal", "VR Sky", Color.parseColor("#9400D3")),
        Effect("moon_falls", "Moon Falls", "VR Sky", Color.parseColor("#FFFFE0")),
        Effect("planet_appears", "Planet Appears", "VR Sky", Color.parseColor("#FF4500")),
        Effect("galaxy_descends", "Galaxy Descends", "VR Sky", Color.parseColor("#4B0082")),
        Effect("meteor_shower_v", "Meteor Shower", "VR Sky", Color.parseColor("#FFD700")),
        Effect("aurora_world", "Aurora World", "VR Sky", Color.parseColor("#00FF7F")),
        Effect("rainbow_tunnel", "Rainbow Tunnel", "VR Sky", Color.parseColor("#FF1493")),
        Effect("cloud_ocean", "Cloud Ocean", "VR Sky", Color.parseColor("#F5F5F5")),
        Effect("floating_clouds", "Floating Clouds", "VR Sky", Color.parseColor("#E6E6FA")),
        Effect("aurora_sky", "Aurora Sky", "VR Sky", Color.parseColor("#00FF7F")),
        Effect("fireworks", "Fireworks", "VR Sky", Color.parseColor("#FF4500")),
        Effect("lightning_storm", "Lightning Storm", "VR Sky", Color.parseColor("#FFFF00")),
        Effect("snow_world", "Snow World", "VR Sky", Color.parseColor("#F5F5F5")),
        Effect("sandstorm", "Sandstorm", "VR Sky", Color.parseColor("#F4A460")),
        Effect("meteor_shower", "Meteor Shower", "VR Sky", Color.parseColor("#FFD700")),

        // ==================== KATEGORI 13: VR Ground ====================
        Effect("ground_becomes_water", "Ground Becomes Water", "VR Ground", Color.parseColor("#0000CD")),
        Effect("ground_becomes_lava", "Ground Becomes Lava", "VR Ground", Color.parseColor("#FF4500")),
        Effect("ground_becomes_glass", "Ground Becomes Glass", "VR Ground", Color.parseColor("#ADD8E6")),
        Effect("ground_becomes_galaxy", "Ground Becomes Galaxy", "VR Ground", Color.parseColor("#4B0082")),
        Effect("ground_opens_portal", "Ground Opens Portal", "VR Ground", Color.parseColor("#9400D3")),
        Effect("ocean_rises", "Ocean Rises", "VR Ground", Color.parseColor("#0000CD")),
        Effect("water_floats", "Water Floats", "VR Ground", Color.parseColor("#00BFFF")),
        Effect("rain_reverses_upward", "Rain Reverses Upward", "VR Ground", Color.parseColor("#4169E1")),
        Effect("snow_freezes_mid_air", "Snow Freezes Mid Air", "VR Ground", Color.parseColor("#F5F5F5")),
        Effect("floating_objects", "Floating Objects", "VR Ground", Color.parseColor("#DDA0DD")),
        Effect("gravity_flip", "Gravity Flip", "VR Ground", Color.parseColor("#FF4500")),
        Effect("zero_gravity", "Zero Gravity", "VR Ground", Color.parseColor("#00FFFF")),
        Effect("earthquake", "Earthquake", "VR Ground", Color.parseColor("#8B4513")),
        Effect("gravity_flip_viral", "Gravity Flip Viral", "VR Ground", Color.parseColor("#FF00FF")),
        Effect("upside_down_world", "Upside Down World", "VR Ground", Color.parseColor("#FFD700")),

        // ==================== KATEGORI 14: VR Weather ====================
        Effect("weather_rain", "Weather Rain", "VR Weather", Color.parseColor("#4169E1")),
        Effect("weather_fog", "Weather Fog", "VR Weather", Color.parseColor("#D3D3D3")),
        Effect("ice_world", "Ice World", "VR Weather", Color.parseColor("#00FFFF")),
        Effect("fire_aura", "Fire Aura", "VR Weather", Color.parseColor("#FF4500")),
        Effect("lightning_power", "Lightning Power", "VR Weather", Color.parseColor("#FFFF00")),
        Effect("ocean_vr", "Ocean VR", "VR Weather", Color.parseColor("#0000CD")),

        // ==================== KATEGORI 15: VR Cinematic ====================
        Effect("cinematic_ai", "Cinematic AI", "VR Cinematic", Color.parseColor("#FFD700")),
        Effect("sunset_ai", "Sunset AI", "VR Cinematic", Color.parseColor("#FF8C00")),
        Effect("cinematic_zoom", "Cinematic Zoom", "VR Cinematic", Color.parseColor("#FFA500")),
        Effect("360_orbit", "360 Orbit", "VR Cinematic", Color.parseColor("#00D4FF")),
        Effect("360_spin", "360 Spin", "VR Cinematic", Color.parseColor("#0088CC")),
        Effect("drone_flyover", "Drone Flyover", "VR Cinematic", Color.parseColor("#87CEEB")),
        Effect("fpv_fly_through", "FPV Fly Through", "VR Cinematic", Color.parseColor("#00CED1")),
        Effect("one_take_orbit", "One Take Orbit", "VR Cinematic", Color.parseColor("#20B2AA")),
        Effect("camera_dive", "Camera Dive", "VR Cinematic", Color.parseColor("#48D1CC")),
        Effect("camera_rise", "Camera Rise", "VR Cinematic", Color.parseColor("#008B8B")),
        Effect("camera_drop", "Camera Drop", "VR Cinematic", Color.parseColor("#00FA9A")),
        Effect("camera_roll", "Camera Roll", "VR Cinematic", Color.parseColor("#66CDAA")),
        Effect("camera_barrel_roll", "Camera Barrel Roll", "VR Cinematic", Color.parseColor("#8FBC8F")),
        Effect("hyper_zoom", "Hyper Zoom", "VR Cinematic", Color.parseColor("#3CB371")),
        Effect("crash_zoom", "Crash Zoom", "VR Cinematic", Color.parseColor("#2E8B57")),
        Effect("slow_push_in", "Slow Push In", "VR Cinematic", Color.parseColor("#006400")),
        Effect("fast_push_in", "Fast Push In", "VR Cinematic", Color.parseColor("#556B2F")),
        Effect("pull_out_reveal", "Pull Out Reveal", "VR Cinematic", Color.parseColor("#6B8E23")),
        Effect("whip_pan", "Whip Pan", "VR Cinematic", Color.parseColor("#9ACD32")),
        Effect("dutch_angle", "Dutch Angle", "VR Cinematic", Color.parseColor("#BDB76B")),
        Effect("spiral_camera", "Spiral Camera", "VR Cinematic", Color.parseColor("#DAA520")),
        Effect("circular_dolly", "Circular Dolly", "VR Cinematic", Color.parseColor("#B8860B")),
        Effect("infinite_zoom", "Infinite Zoom", "VR Cinematic", Color.parseColor("#CD853F")),

        // ==================== KATEGORI 16: VR Camera ====================
        Effect("portal_teleport", "Portal Teleport", "VR Camera", Color.parseColor("#9400D3")),
        Effect("door_teleport", "Door Teleport", "VR Camera", Color.parseColor("#8B4513")),
        Effect("mirror_teleport", "Mirror Teleport", "VR Camera", Color.parseColor("#C0C0C0")),
        Effect("wall_teleport", "Wall Teleport", "VR Camera", Color.parseColor("#808080")),
        Effect("ground_portal", "Ground Portal", "VR Camera", Color.parseColor("#228B22")),
        Effect("sky_portal", "Sky Portal", "VR Camera", Color.parseColor("#87CEEB")),
        Effect("dimension_jump", "Dimension Jump", "VR Camera", Color.parseColor("#FF00FF")),
        Effect("reality_glitch_v", "Reality Glitch", "VR Camera", Color.parseColor("#00FF00")),
        Effect("blink_transition", "Blink Transition", "VR Camera", Color.parseColor("#000000")),
        Effect("flash_transition", "Flash Transition", "VR Camera", Color.parseColor("#FFFFFF")),
        Effect("smoke_transition", "Smoke Transition", "VR Camera", Color.parseColor("#808080")),
        Effect("fire_transition", "Fire Transition", "VR Camera", Color.parseColor("#FF4500")),
        Effect("water_transition", "Water Transition", "VR Camera", Color.parseColor("#0000CD")),
        Effect("lightning_transition", "Lightning Transition", "VR Camera", Color.parseColor("#FFFF00")),
        Effect("glass_shatter_transition", "Glass Shatter Transition", "VR Camera", Color.parseColor("#ADD8E6")),
        Effect("pixel_transition", "Pixel Transition", "VR Camera", Color.parseColor("#00FF00")),
        Effect("digital_scan_transition", "Digital Scan Transition", "VR Camera", Color.parseColor("#00D4FF")),
        Effect("black_hole_transition", "Black Hole Transition", "VR Camera", Color.parseColor("#000000")),

        // ==================== KATEGORI 17: VR Teleport ====================
        Effect("gravity_reverse", "Gravity Reverse", "VR Teleport", Color.parseColor("#FF00FF")),
        Effect("gravity_zero", "Gravity Zero", "VR Teleport", Color.parseColor("#00FFFF")),
        Effect("world_rotation", "World Rotation", "VR Teleport", Color.parseColor("#FFD700")),
        Effect("time_freeze_v", "Time Freeze", "VR Teleport", Color.parseColor("#00FFFF")),
        Effect("time_reverse", "Time Reverse", "VR Teleport", Color.parseColor("#FF4500")),
        Effect("time_warp", "Time Warp", "VR Teleport", Color.parseColor("#9400D3")),
        Effect("speed_ramp", "Speed Ramp", "VR Teleport", Color.parseColor("#FF1493")),
        Effect("slow_motion", "Slow Motion", "VR Teleport", Color.parseColor("#4169E1")),
        Effect("hyperlapse", "Hyperlapse", "VR Teleport", Color.parseColor("#FFA500")),
        Effect("infinite_loop", "Infinite Loop", "VR Teleport", Color.parseColor("#FF00FF")),
        Effect("endless_corridor", "Endless Corridor", "VR Teleport", Color.parseColor("#808080")),
        Effect("infinite_staircase", "Infinite Staircase", "VR Teleport", Color.parseColor("#DEB887")),
        Effect("infinite_room_v", "Infinite Room", "VR Teleport", Color.parseColor("#DDA0DD")),
        Effect("infinite_city", "Infinite City", "VR Teleport", Color.parseColor("#708090")),
        Effect("parallel_universe_v", "Parallel Universe", "VR Teleport", Color.parseColor("#4B0082")),
        Effect("world_folding", "World Folding", "VR Teleport", Color.parseColor("#FF4500")),
        Effect("reality_melting", "Reality Melting", "VR Teleport", Color.parseColor("#FF1493")),
        Effect("space_bending", "Space Bending", "VR Teleport", Color.parseColor("#9400D3")),
        Effect("perspective_shift", "Perspective Shift", "VR Teleport", Color.parseColor("#00D4FF")),

        // ==================== KATEGORI 18: VR Character ====================
        Effect("clone_army", "Clone Army", "VR Character", Color.parseColor("#00FF00")),
        Effect("giant_character", "Giant Character", "VR Character", Color.parseColor("#FF4500")),
        Effect("tiny_character", "Tiny Character", "VR Character", Color.parseColor("#FF69B4")),
        Effect("character_levitation", "Character Levitation", "VR Character", Color.parseColor("#9400D3")),
        Effect("character_teleport", "Character Teleport", "VR Character", Color.parseColor("#00FFFF")),
        Effect("character_disappear", "Character Disappear", "VR Character", Color.parseColor("#2F4F4F")),
        Effect("character_reappear", "Character Reappear", "VR Character", Color.parseColor("#00FF00")),
        Effect("character_hologram", "Character Hologram", "VR Character", Color.parseColor("#00FFFF")),
        Effect("character_glitch", "Character Glitch", "VR Character", Color.parseColor("#FF00FF")),
        Effect("character_pixelate", "Character Pixelate", "VR Character", Color.parseColor("#00FF00")),
        Effect("character_turn_to_stone", "Turn to Stone", "VR Character", Color.parseColor("#696969")),
        Effect("character_turn_to_glass", "Turn to Glass", "VR Character", Color.parseColor("#ADD8E6")),
        Effect("character_turn_to_crystal", "Turn to Crystal", "VR Character", Color.parseColor("#E0FFFF")),
        Effect("character_turn_to_smoke", "Turn to Smoke", "VR Character", Color.parseColor("#808080")),
        Effect("character_turn_to_fire", "Turn to Fire", "VR Character", Color.parseColor("#FF4500")),
        Effect("character_turn_to_water", "Turn to Water", "VR Character", Color.parseColor("#0000CD")),
        Effect("character_turn_to_lightning", "Turn to Lightning", "VR Character", Color.parseColor("#FFFF00")),
        Effect("character_turn_to_particles", "Turn to Particles", "VR Character", Color.parseColor("#FFD700")),
        Effect("character_digital_scan", "Digital Scan", "VR Character", Color.parseColor("#00FF00")),
        Effect("character_shadow_clone", "Shadow Clone", "VR Character", Color.parseColor("#2F4F4F")),

        // ==================== KATEGORI 19: Klasik ====================
        Effect("vintage", "Vintage", "Klasik", Color.parseColor("#DEB887")),
        Effect("neon", "Neon", "Klasik", Color.parseColor("#FF00FF")),
        Effect("glitch", "Glitch", "Klasik", Color.parseColor("#FF0000")),
        Effect("thermal", "Thermal", "Klasik", Color.parseColor("#FF4500")),
        Effect("emboss", "Emboss", "Klasik", Color.parseColor("#CD853F")),
        Effect("sketch", "Sketch", "Klasik", Color.parseColor("#FFFFFF")),
        Effect("wave", "Wave", "Klasik", Color.parseColor("#00BFFF")),
        Effect("cartoon", "Cartoon", "Klasik", Color.parseColor("#ADFF2F")),
        Effect("mirror", "Mirror", "Klasik", Color.parseColor("#FF6347")),
        Effect("color_shift", "Color Shift", "Klasik", Color.parseColor("#FF1493")),
        Effect("sepia", "Sepia", "Klasik", Color.parseColor("#DEB887")),
        Effect("invert", "Invert", "Klasik", Color.parseColor("#FF1493")),
        Effect("pixelate", "Pixelate", "Klasik", Color.parseColor("#FF69B4")),
        Effect("edge_detect", "Edge Detect", "Klasik", Color.parseColor("#00FF00")),
        Effect("hologram", "Hologram", "Klasik", Color.parseColor("#00FFFF")),
        Effect("neon_cyberpunk", "Neon Cyberpunk", "Klasik", Color.parseColor("#FF00FF")),
        Effect("digital_glitch", "Digital Glitch", "Klasik", Color.parseColor("#00FF00")),
        Effect("rgb_split", "RGB Split", "Klasik", Color.parseColor("#FF0000")),
        Effect("vhs_retro", "VHS Retro", "Klasik", Color.parseColor("#FF8C00")),
        Effect("matrix_rain", "Matrix Rain", "Klasik", Color.parseColor("#00FF00")),

        // ==================== KATEGORI 20: TikTok Viral ====================
        Effect("heart_rain", "Heart Rain", "TikTok Viral", Color.parseColor("#FF0000")),
        Effect("star_rain", "Star Rain", "TikTok Viral", Color.parseColor("#FFD700")),
        Effect("sparkle", "Sparkle", "TikTok Viral", Color.parseColor("#FFFFFF")),
        Effect("butterfly", "Butterfly", "TikTok Viral", Color.parseColor("#FF69B4")),
        Effect("magic_sparkle", "Magic Sparkle", "TikTok Viral", Color.parseColor("#FFD700")),
        Effect("energy_aura", "Energy Aura", "TikTok Viral", Color.parseColor("#00FFFF")),
        Effect("magic_spell", "Magic Spell", "TikTok Viral", Color.parseColor("#9400D3")),
        Effect("dragon_fire", "Dragon Fire", "TikTok Viral", Color.parseColor("#FF4500")),
        Effect("electric_shock", "Electric Shock", "TikTok Viral", Color.parseColor("#FFFF00")),
        Effect("magic_circle", "Magic Circle", "TikTok Viral", Color.parseColor("#FFD700")),
        Effect("particle_explosion", "Particle Explosion", "TikTok Viral", Color.parseColor("#FF4500")),
        Effect("rainbow_energy", "Rainbow Energy", "TikTok Viral", Color.parseColor("#FF1493")),
        Effect("phoenix_wings", "Phoenix Wings", "TikTok Viral", Color.parseColor("#FF4500")),
        Effect("angel_wings", "Angel Wings", "TikTok Viral", Color.parseColor("#FFFFFF")),
        Effect("devil_wings", "Devil Wings", "TikTok Viral", Color.parseColor("#DC143C")),
        Effect("floating_text", "Floating Text", "TikTok Viral", Color.parseColor("#FFD700")),
        Effect("orbiting_planets", "Orbiting Planets", "TikTok Viral", Color.parseColor("#87CEEB")),
        Effect("mini_planet", "Mini Planet", "TikTok Viral", Color.parseColor("#228B22")),

        // ==================== KATEGORI 21: Weather Effects ====================
        Effect("rain_overlay", "Rain Overlay", "Weather", Color.parseColor("#4169E1")),
        Effect("snow_overlay", "Snow Overlay", "Weather", Color.parseColor("#F5F5F5")),
        Effect("fog_overlay", "Fog Overlay", "Weather", Color.parseColor("#D3D3D3")),
        Effect("lightning_overlay", "Lightning Overlay", "Weather", Color.parseColor("#FFFF00")),
        Effect("wind_effect", "Wind Effect", "Weather", Color.parseColor("#B0C4DE")),
        Effect("rainbow_effect", "Rainbow Effect", "Weather", Color.parseColor("#FF1493")),

        // ==================== KATEGORI 22: Special Effects ====================
        Effect("lens_flare", "Lens Flare", "Special", Color.parseColor("#FFD700")),
        Effect("bokeh", "Bokeh", "Special", Color.parseColor("#FF69B4")),
        Effect("light_leak", "Light Leak", "Special", Color.parseColor("#FF8C00")),
        Effect("film_grain", "Film Grain", "Special", Color.parseColor("#808080")),
        Effect("chromatic_aberration", "Chromatic Aberration", "Special", Color.parseColor("#FF00FF")),
        Effect("vignette", "Vignette", "Special", Color.parseColor("#000000")),
        Effect("bloom", "Bloom", "Special", Color.parseColor("#FFFFFF")),
        Effect("motion_trail", "Motion Trail", "Special", Color.parseColor("#00FFFF")),
        Effect("ghost_trail", "Ghost Trail", "Special", Color.parseColor("#C0C0C0")),
        Effect("time_slice", "Time Slice", "Special", Color.parseColor("#9400D3")),

        // ==================== KATEGORI 23: Retro Effects ====================
        Effect("vhs_tracking", "VHS Tracking", "Retro", Color.parseColor("#FF0000")),
        Effect("crt_monitor", "CRT Monitor", "Retro", Color.parseColor("#00FF00")),
        Effect("scanlines", "Scanlines", "Retro", Color.parseColor("#808080")),
        Effect("old_tv", "Old TV", "Retro", Color.parseColor("#D3D3D3")),
        Effect("polaroid", "Polaroid", "Retro", Color.parseColor("#DEB887")),
        Effect("film_reel", "Film Reel", "Retro", Color.parseColor("#2F4F4F")),
        Effect("vintage_camera", "Vintage Camera", "Retro", Color.parseColor("#8B4513")),
        Effect("instant_photo", "Instant Photo", "Retro", Color.parseColor("#FFA500")),

        // ==================== KATEGORI 24: Neon Effects ====================
        Effect("neon_border", "Neon Border", "Neon", Color.parseColor("#FF00FF")),
        Effect("neon_glow", "Neon Glow", "Neon", Color.parseColor("#00FFFF")),
        Effect("neon_pulse", "Neon Pulse", "Neon", Color.parseColor("#FF1493")),
        Effect("neon_flicker", "Neon Flicker", "Neon", Color.parseColor("#FFD700")),
        Effect("neon_strobe", "Neon Strobe", "Neon", Color.parseColor("#FFFFFF")),
        Effect("neon_wave", "Neon Wave", "Neon", Color.parseColor("#00FF00")),

        // ==================== KATEGORI 25: Color Effects ====================
        Effect("color_isolation", "Color Isolation", "Color", Color.parseColor("#FF0000")),
        Effect("color_pop", "Color Pop", "Color", Color.parseColor("#FFD700")),
        Effect("duotone", "Duotone", "Color", Color.parseColor("#FF1493")),
        Effect("tritone", "Tritone", "Color", Color.parseColor("#00FFFF")),
        Effect("color_balance", "Color Balance", "Color", Color.parseColor("#00FF00")),
        Effect("hue_shift", "Hue Shift", "Color", Color.parseColor("#FF00FF")),
        Effect("saturation_boost", "Saturation Boost", "Color", Color.parseColor("#FF4500")),
        Effect("contrast_boost", "Contrast Boost", "Color", Color.parseColor("#0000FF")),

        // ==================== KATEGORI 26: Distortion Effects ====================
        Effect("fisheye", "Fisheye", "Distortion", Color.parseColor("#00FFFF")),
        Effect("spherize", "Spherize", "Distortion", Color.parseColor("#FF69B4")),
        Effect("swirl", "Swirl", "Distortion", Color.parseColor("#9400D3")),
        Effect("bulge", "Bulge", "Distortion", Color.parseColor("#FF1493")),
        Effect("pinch", "Pinch", "Distortion", Color.parseColor("#00FF00")),
        Effect("wave_distortion", "Wave Distortion", "Distortion", Color.parseColor("#00BFFF")),
        Effect("ripple", "Ripple", "Distortion", Color.parseColor("#4169E1")),
        Effect("glass_distortion", "Glass Distortion", "Distortion", Color.parseColor("#ADD8E6")),

        // ==================== KATEGORI 27: Artistic Effects ====================
        Effect("oil_painting", "Oil Painting", "Artistic", Color.parseColor("#FF8C00")),
        Effect("watercolor", "Watercolor", "Artistic", Color.parseColor("#87CEEB")),
        Effect("pencil_sketch", "Pencil Sketch", "Artistic", Color.parseColor("#808080")),
        Effect("charcoal", "Charcoal", "Artistic", Color.parseColor("#2F4F4F")),
        Effect("pop_art", "Pop Art", "Artistic", Color.parseColor("#FF1493")),
        Effect("impressionist", "Impressionist", "Artistic", Color.parseColor("#FFD700")),
        Effect("stained_glass", "Stained Glass", "Artistic", Color.parseColor("#FF4500")),
        Effect("mosaic", "Mosaic", "Artistic", Color.parseColor("#00FF00")),

        // ==================== KATEGORI 28: Glitch Effects ====================
        Effect("pixel_sort", "Pixel Sort", "Glitch", Color.parseColor("#FF00FF")),
        Effect("data_mosh", "Data Mosh", "Glitch", Color.parseColor("#00FFFF")),
        Effect("bit_crush", "Bit Crush", "Glitch", Color.parseColor("#FF4500")),
        Effect("corruption", "Corruption", "Glitch", Color.parseColor("#00FF00")),
        Effect("tear", "Tear", "Glitch", Color.parseColor("#FFD700")),
        Effect("stutter", "Stutter", "Glitch", Color.parseColor("#FF1493")),
        Effect("artifact", "Artifact", "Glitch", Color.parseColor("#808080")),
        Effect("noise", "Noise", "Glitch", Color.parseColor("#FFFFFF")),

        // ==================== KATEGORI 29: Sci-Fi Effects ====================
        Effect("holographic", "Holographic", "Sci-Fi", Color.parseColor("#00FFFF")),
        Effect("cyber_scan", "Cyber Scan", "Sci-Fi", Color.parseColor("#00FF00")),
        Effect("digital_rain", "Digital Rain", "Sci-Fi", Color.parseColor("#00FF00")),
        Effect("matrix_code", "Matrix Code", "Sci-Fi", Color.parseColor("#00FF00")),
        Effect("ai_overlay", "AI Overlay", "Sci-Fi", Color.parseColor("#00D4FF")),
        Effect("hud_display", "HUD Display", "Sci-Fi", Color.parseColor("#00FFFF")),
        Effect("target_lock", "Target Lock", "Sci-Fi", Color.parseColor("#FF0000")),
        Effect("scanner_beam", "Scanner Beam", "Sci-Fi", Color.parseColor("#00FF00")),

        // ==================== KATEGORI 30: Fantasy Effects ====================
        Effect("fairy_dust", "Fairy Dust", "Fantasy", Color.parseColor("#FFD700")),
        Effect("magic_wand", "Magic Wand", "Fantasy", Color.parseColor("#9400D3")),
        Effect("enchantment", "Enchantment", "Fantasy", Color.parseColor("#FF69B4")),
        Effect("crystal_ball", "Crystal Ball", "Fantasy", Color.parseColor("#E0FFFF")),
        Effect("potion_brew", "Potion Brew", "Fantasy", Color.parseColor("#00FF00")),
        Effect("dragon_breath", "Dragon Breath", "Fantasy", Color.parseColor("#FF4500")),
        Effect("ice_magic", "Ice Magic", "Fantasy", Color.parseColor("#00FFFF")),
        Effect("fire_magic", "Fire Magic", "Fantasy", Color.parseColor("#FF4500")),
        Effect("lightning_magic", "Lightning Magic", "Fantasy", Color.parseColor("#FFFF00")),
        Effect("nature_magic", "Nature Magic", "Fantasy", Color.parseColor("#228B22"))
    )

    fun getCategories(): List<String> {
        return effects.map { it.category }.distinct()
    }

    fun getEffectsByCategory(category: String): List<Effect> {
        return effects.filter { it.category == category }
    }

    fun applyEffect(bitmap: Bitmap, effectId: String): Bitmap {
        val result = bitmap.copy(Bitmap.Config.ARGB_8888, true)
        val width = result.width
        val height = result.height
        val pixels = IntArray(width * height)
        result.getPixels(pixels, 0, width, 0, 0, width, height)

        when (effectId) {
            // Basic effects
            "vintage" -> applyVintage(pixels, width, height)
            "sepia" -> applySepia(pixels, width, height)
            "grayscale" -> applyGrayscale(pixels, width, height)
            "invert" -> applyInvert(pixels, width, height)
            "neon" -> applyNeon(pixels, width, height)
            "emboss" -> applyEmboss(pixels, width, height)
            "sketch" -> applySketch(pixels, width, height)
            "cartoon" -> applyCartoon(pixels, width, height)
            "pixelate" -> applyPixelate(pixels, width, height)
            "edge_detect" -> applyEdgeDetect(pixels, width, height)
            "mirror" -> applyMirror(pixels, width, height)
            "thermal" -> applyThermal(pixels, width, height)
            "glitch" -> applyGlitch(pixels, width, height)
            "wave" -> applyWave(pixels, width, height)
            "color_shift" -> applyColorShift(pixels, width, height)
            "hologram" -> applyHologram(pixels, width, height)
            "neon_cyberpunk" -> applyNeonCyberpunk(pixels, width, height)
            "digital_glitch" -> applyDigitalGlitch(pixels, width, height)
            "rgb_split" -> applyRGBSplit(pixels, width, height)
            "vhs_retro" -> applyVHSRetro(pixels, width, height)
            "matrix_rain" -> applyMatrixRain(pixels, width, height)

            // Weather
            "weather_rain" -> applyRainOverlay(pixels, width, height)
            "snow_world" -> applySnowOverlay(pixels, width, height)
            "weather_fog" -> applyFogOverlay(pixels, width, height)
            "lightning_storm" -> applyLightningOverlay(pixels, width, height)
            "aurora_sky" -> applyAuroraEffect(pixels, width, height)
            "rainbow_tunnel" -> applyRainbowEffect(pixels, width, height)

            // Water & Ocean
            "ocean_vr" -> applyOceanEffect(pixels, width, height)
            "water_portal" -> applyWaterEffect(pixels, width, height)
            "ice_world" -> applyIceEffect(pixels, width, height)
            "ice_portal" -> applyIceEffect(pixels, width, height)

            // Fire & Energy
            "fire_portal" -> applyFireEffect(pixels, width, height)
            "fire_aura" -> applyFireEffect(pixels, width, height)
            "dragon_fire" -> applyFireEffect(pixels, width, height)
            "energy_aura" -> applyEnergyAura(pixels, width, height)
            "electric_shock" -> applyElectricShock(pixels, width, height)

            // Space & Galaxy
            "galaxy_portal" -> applyGalaxyEffect(pixels, width, height)
            "galaxy_eyes" -> applyGalaxyEffect(pixels, width, height)
            "galaxy_mirror" -> applyGalaxyEffect(pixels, width, height)
            "galaxy_eye" -> applyGalaxyEffect(pixels, width, height)
            "cosmic_reflection" -> applyGalaxyEffect(pixels, width, height)

            // Portal & Dimension
            "vr_portal" -> applyPortalEffect(pixels, width, height)
            "teleport_portal" -> applyPortalEffect(pixels, width, height)
            "mirror_dimension" -> applyMirrorDimension(pixels, width, height)
            "mirror_dimension_v" -> applyMirrorDimension(pixels, width, height)
            "portal_effect" -> applyPortalEffect(pixels, width, height)
            "magic_door" -> applyPortalEffect(pixels, width, height)
            "mirror_portal" -> applyMirrorDimension(pixels, width, height)
            "dimension_rift" -> applyPortalEffect(pixels, width, height)
            "black_hole" -> applyBlackHole(pixels, width, height)
            "black_hole_portal" -> applyBlackHole(pixels, width, height)
            "wormhole" -> applyWormhole(pixels, width, height)
            "wormhole_jump" -> applyWormhole(pixels, width, height)

            // Robot & AI
            "robot" -> applyRobotEffect(pixels, width, height)
            "robot_vision" -> applyRobotVision(pixels, width, height)
            "cyber_eye" -> applyRobotVision(pixels, width, height)

            // Cyberpunk
            "cyberpunk" -> applyCyberpunkEffect(pixels, width, height)
            "cyberpunk_hud" -> applyCyberpunkHUD(pixels, width, height)
            "neon_vision" -> applyNeonVision(pixels, width, height)
            "futuristic_city" -> applyCyberpunkEffect(pixels, width, height)
            "neon_night" -> applyCyberpunkEffect(pixels, width, height)
            "cyber_portal" -> applyCyberpunkEffect(pixels, width, height)
            "cyber_mirror" -> applyCyberpunkEffect(pixels, width, height)

            // Horror
            "horror_night" -> applyHorrorEffect(pixels, width, height)
            "creepy_dark" -> applyHorrorEffect(pixels, width, height)
            "ghost_appears" -> applyHorrorEffect(pixels, width, height)

            // Night Vision
            "night_vision" -> applyNightVision(pixels, width, height)
            "thermal_vision" -> applyThermalVision(pixels, width, height)
            "xray_world" -> applyXRayEffect(pixels, width, height)
            "infrared_world" -> applyInfraredEffect(pixels, width, height)
            "digital_vision" -> applyDigitalVision(pixels, width, height)
            "matrix_vision" -> applyMatrixVision(pixels, width, height)
            "glitch_vision" -> applyGlitchVision(pixels, width, height)
            "dream_vision" -> applyDreamVision(pixels, width, height)
            "future_vision" -> applyFutureVision(pixels, width, height)
            "quantum_vision" -> applyQuantumVision(pixels, width, height)

            // VFX
            "cinematic_ai" -> applyCinematicEffect(pixels, width, height)
            "sunset_ai" -> applySunsetEffect(pixels, width, height)

            // Portrait
            "beauty_ai" -> applyBeautyEffect(pixels, width, height)
            "face_scan" -> applyFaceScanEffect(pixels, width, height)

            // Default - return original
            else -> { /* No change */ }
        }

        result.setPixels(pixels, 0, width, 0, 0, width, height)
        return result
    }

    // ==================== EFFECT IMPLEMENTATIONS ====================

    private fun applyVintage(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.393 + g * 0.769 + b * 0.189).toInt().coerceIn(0, 255)
            val newG = (r * 0.349 + g * 0.686 + b * 0.168).toInt().coerceIn(0, 255)
            val newB = (r * 0.272 + g * 0.534 + b * 0.131).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applySepia(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val newR = (gray + 40).coerceIn(0, 255)
            val newG = (gray + 20).coerceIn(0, 255)
            val newB = gray.coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyGrayscale(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            pixels[i] = Color.argb(Color.alpha(pixels[i]), gray, gray, gray)
        }
    }

    private fun applyInvert(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = 255 - Color.red(pixels[i])
            val g = 255 - Color.green(pixels[i])
            val b = 255 - Color.blue(pixels[i])
            pixels[i] = Color.argb(Color.alpha(pixels[i]), r, g, b)
        }
    }

    private fun applyNeon(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val brightness = (r + g + b) / 3
            val factor = if (brightness > 128) 1.5f else 0.5f
            val newR = (r * factor).toInt().coerceIn(0, 255)
            val newG = (g * factor).toInt().coerceIn(0, 255)
            val newB = (b * factor).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyEmboss(pixels: IntArray, width: Int, height: Int) {
        val temp = pixels.copyOf()
        for (y in 1 until height - 1) {
            for (x in 1 until width - 1) {
                val idx = y * width + x
                val top = temp[(y - 1) * width + x]
                val left = temp[y * width + (x - 1)]
                val r = (Color.red(top) - Color.red(left) + 128).coerceIn(0, 255)
                val g = (Color.green(top) - Color.green(left) + 128).coerceIn(0, 255)
                val b = (Color.blue(top) - Color.blue(left) + 128).coerceIn(0, 255)
                pixels[idx] = Color.argb(Color.alpha(pixels[idx]), r, g, b)
            }
        }
    }

    private fun applySketch(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val sketch = if (gray > 128) 255 else 0
            pixels[i] = Color.argb(Color.alpha(pixels[i]), sketch, sketch, sketch)
        }
    }

    private fun applyCartoon(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r / 32) * 32
            val newG = (g / 32) * 32
            val newB = (b / 32) * 32
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyPixelate(pixels: IntArray, width: Int, height: Int) {
        val blockSize = 10
        for (y in 0 until height step blockSize) {
            for (x in 0 until width step blockSize) {
                val idx = y * width + x
                if (idx < pixels.size) {
                    val color = pixels[idx]
                    for (dy in 0 until blockSize) {
                        for (dx in 0 until blockSize) {
                            val nx = x + dx
                            val ny = y + dy
                            if (nx < width && ny < height) {
                                pixels[ny * width + nx] = color
                            }
                        }
                    }
                }
            }
        }
    }

    private fun applyEdgeDetect(pixels: IntArray, width: Int, height: Int) {
        val temp = pixels.copyOf()
        for (y in 1 until height - 1) {
            for (x in 1 until width - 1) {
                val idx = y * width + x
                val top = temp[(y - 1) * width + x]
                val bottom = temp[(y + 1) * width + x]
                val left = temp[y * width + (x - 1)]
                val right = temp[y * width + (x + 1)]
                val r = (Math.abs(Color.red(top) - Color.red(bottom)) +
                        Math.abs(Color.red(left) - Color.red(right))).coerceIn(0, 255)
                val g = (Math.abs(Color.green(top) - Color.green(bottom)) +
                        Math.abs(Color.green(left) - Color.green(right))).coerceIn(0, 255)
                val b = (Math.abs(Color.blue(top) - Color.blue(bottom)) +
                        Math.abs(Color.blue(left) - Color.blue(right))).coerceIn(0, 255)
                pixels[idx] = Color.argb(Color.alpha(pixels[idx]), r, g, b)
            }
        }
    }

    private fun applyMirror(pixels: IntArray, width: Int, height: Int) {
        val temp = pixels.copyOf()
        for (y in 0 until height) {
            for (x in 0 until width / 2) {
                val mirrorX = width - 1 - x
                pixels[y * width + x] = temp[y * width + mirrorX]
            }
        }
    }

    private fun applyThermal(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val temp = (r + g + b) / 3
            val newR = (temp * 2).coerceIn(0, 255)
            val newG = if (temp > 128) (255 - temp) * 2 else 0
            val newB = if (temp < 128) (128 - temp) * 2 else 0
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR.toInt(), newG.toInt(), newB.toInt())
        }
    }

    private fun applyGlitch(pixels: IntArray, width: Int, height: Int) {
        val shift = Random.nextInt(-20, 20)
        val temp = pixels.copyOf()
        for (y in 0 until height) {
            if (Random.nextFloat() < 0.1f) {
                for (x in 0 until width) {
                    val newX = (x + shift).coerceIn(0, width - 1)
                    pixels[y * width + x] = temp[y * width + newX]
                }
            }
        }
    }

    private fun applyWave(pixels: IntArray, width: Int, height: Int) {
        val temp = pixels.copyOf()
        for (y in 0 until height) {
            val shift = (Math.sin(y * 0.05) * 20).toInt()
            for (x in 0 until width) {
                val newX = (x + shift).coerceIn(0, width - 1)
                pixels[y * width + x] = temp[y * width + newX]
            }
        }
    }

    private fun applyColorShift(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            pixels[i] = Color.argb(Color.alpha(pixels[i]), g, b, r)
        }
    }

    private fun applyHologram(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val y = i / width
            val scanline = if (y % 4 == 0) 0.7f else 1.0f
            val newR = (r * 0.2 * scanline).toInt().coerceIn(0, 255)
            val newG = (g * 0.8 * scanline).toInt().coerceIn(0, 255)
            val newB = (b * 0.8 * scanline).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyNeonCyberpunk(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.5 + 128 * 0.5).toInt().coerceIn(0, 255)
            val newG = (g * 0.3).toInt().coerceIn(0, 255)
            val newB = (b * 1.5).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyDigitalGlitch(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            if (Random.nextFloat() < 0.05f) {
                val r = Random.nextInt(0, 256)
                val g = Random.nextInt(0, 256)
                val b = Random.nextInt(0, 256)
                pixels[i] = Color.argb(Color.alpha(pixels[i]), r, g, b)
            }
        }
    }

    private fun applyRGBSplit(pixels: IntArray, width: Int, height: Int) {
        val temp = pixels.copyOf()
        val offset = 5
        for (y in 0 until height) {
            for (x in 0 until width) {
                val idx = y * width + x
                val rIdx = y * width + (x + offset).coerceIn(0, width - 1)
                val bIdx = y * width + (x - offset).coerceIn(0, width - 1)
                val r = Color.red(temp[rIdx])
                val g = Color.green(temp[idx])
                val b = Color.blue(temp[bIdx])
                pixels[idx] = Color.argb(Color.alpha(pixels[idx]), r, g, b)
            }
        }
    }

    private fun applyVHSRetro(pixels: IntArray, width: Int, height: Int) {
        for (y in 0 until height) {
            if (Random.nextFloat() < 0.02f) {
                val shift = Random.nextInt(-10, 10)
                for (x in 0 until width) {
                    val newX = (x + shift).coerceIn(0, width - 1)
                    pixels[y * width + x] = pixels[y * width + newX]
                }
            }
        }
        for (i in pixels.indices) {
            val noise = Random.nextInt(-10, 10)
            val r = (Color.red(pixels[i]) + noise).coerceIn(0, 255)
            val g = (Color.green(pixels[i]) + noise).coerceIn(0, 255)
            val b = (Color.blue(pixels[i]) + noise).coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), r, g, b)
        }
    }

    private fun applyMatrixRain(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val newR = 0
            val newG = gray
            val newB = 0
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyRainOverlay(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val y = i / width
            if (y % 8 == 0) {
                val r = (Color.red(pixels[i]) * 0.7).toInt()
                val g = (Color.green(pixels[i]) * 0.7 + 30).toInt().coerceIn(0, 255)
                val b = (Color.blue(pixels[i]) * 0.7 + 60).toInt().coerceIn(0, 255)
                pixels[i] = Color.argb(Color.alpha(pixels[i]), r, g, b)
            }
        }
    }

    private fun applySnowOverlay(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            if (Random.nextFloat() < 0.01f) {
                pixels[i] = Color.WHITE
            }
        }
    }

    private fun applyFogOverlay(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.6 + 200 * 0.4).toInt()
            val newG = (g * 0.6 + 200 * 0.4).toInt()
            val newB = (b * 0.6 + 200 * 0.4).toInt()
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyLightningOverlay(pixels: IntArray, width: Int, height: Int) {
        if (Random.nextFloat() < 0.1f) {
            for (i in pixels.indices) {
                pixels[i] = Color.WHITE
            }
        }
    }

    private fun applyAuroraEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val y = i / width
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val aurora = (Math.sin(y * 0.02) * 50 + 50).toInt()
            val newR = (r * 0.5 + aurora * 0.5).toInt().coerceIn(0, 255)
            val newG = (g * 0.5 + aurora * 1.5).toInt().coerceIn(0, 255)
            val newB = (b * 0.5 + aurora * 0.8).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyRainbowEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val y = i / width
            val hue = (y * 360.0 / height).toFloat()
            val hsv = floatArrayOf(hue, 1.0f, 1.0f)
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114) / 255.0f
            val rainbow = Color.HSVToColor(floatArrayOf(hsv[0], hsv[1], gray))
            pixels[i] = Color.argb(Color.alpha(pixels[i]),
                Color.red(rainbow), Color.green(rainbow), Color.blue(rainbow))
        }
    }

    private fun applyOceanEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.5).toInt().coerceIn(0, 255)
            val newG = (g * 0.7 + 30).toInt().coerceIn(0, 255)
            val newB = (b * 1.2 + 50).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyWaterEffect(pixels: IntArray, width: Int, height: Int) {
        applyOceanEffect(pixels, width, height)
    }

    private fun applyIceEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.6 + 100 * 0.4).toInt().coerceIn(0, 255)
            val newG = (g * 0.6 + 200 * 0.4).toInt().coerceIn(0, 255)
            val newB = (b * 0.6 + 255 * 0.4).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyFireEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 1.3 + 50).toInt().coerceIn(0, 255)
            val newG = (g * 0.5).toInt().coerceIn(0, 255)
            val newB = (b * 0.2).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyEnergyAura(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val brightness = (r + g + b) / 3
            val newR = (brightness * 0.3).toInt().coerceIn(0, 255)
            val newG = (brightness * 0.8 + 50).toInt().coerceIn(0, 255)
            val newB = (brightness * 1.2 + 100).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyElectricShock(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            if (Random.nextFloat() < 0.02f) {
                pixels[i] = Color.YELLOW
            }
        }
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = r.coerceIn(0, 255)
            val newG = (g * 0.8 + 30).toInt().coerceIn(0, 255)
            val newB = b.coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyGalaxyEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.3 + 75 * 0.7).toInt().coerceIn(0, 255)
            val newG = (g * 0.3 + 0 * 0.7).toInt().coerceIn(0, 255)
            val newB = (b * 0.3 + 130 * 0.7).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyPortalEffect(pixels: IntArray, width: Int, height: Int) {
        val cx = width / 2
        val cy = height / 2
        for (y in 0 until height) {
            for (x in 0 until width) {
                val idx = y * width + x
                val dx = x - cx
                val dy = y - cy
                val dist = Math.sqrt((dx * dx + dy * dy).toDouble())
                val angle = Math.atan2(dy.toDouble(), dx.toDouble())
                val hue = ((angle * 180 / Math.PI + 180) % 360).toFloat()
                val saturation = (1.0 - dist / (width / 2)).coerceIn(0.0, 1.0).toFloat()
                val hsv = floatArrayOf(hue, saturation, 1.0f)
                val portalColor = Color.HSVToColor(hsv)
                val r = (Color.red(pixels[idx]) * 0.5 + Color.red(portalColor) * 0.5).toInt()
                val g = (Color.green(pixels[idx]) * 0.5 + Color.green(portalColor) * 0.5).toInt()
                val b = (Color.blue(pixels[idx]) * 0.5 + Color.blue(portalColor) * 0.5).toInt()
                pixels[idx] = Color.argb(Color.alpha(pixels[idx]), r, g, b)
            }
        }
    }

    private fun applyMirrorDimension(pixels: IntArray, width: Int, height: Int) {
        val temp = pixels.copyOf()
        for (y in 0 until height) {
            for (x in 0 until width) {
                val mirrorX = width - 1 - x
                val mirrorY = height - 1 - y
                if ((x + y) % 2 == 0) {
                    pixels[y * width + x] = temp[y * width + mirrorX]
                } else {
                    pixels[y * width + x] = temp[mirrorY * width + x]
                }
            }
        }
    }

    private fun applyBlackHole(pixels: IntArray, width: Int, height: Int) {
        val cx = width / 2
        val cy = height / 2
        for (y in 0 until height) {
            for (x in 0 until width) {
                val idx = y * width + x
                val dx = x - cx
                val dy = y - cy
                val dist = Math.sqrt((dx * dx + dy * dy).toDouble())
                val maxDist = Math.sqrt((cx * cx + cy * cy).toDouble())
                val factor = (1.0 - dist / maxDist).coerceIn(0.0, 1.0)
                val r = (Color.red(pixels[idx]) * factor).toInt()
                val g = (Color.green(pixels[idx]) * factor).toInt()
                val b = (Color.blue(pixels[idx]) * factor).toInt()
                pixels[idx] = Color.argb(Color.alpha(pixels[idx]), r, g, b)
            }
        }
    }

    private fun applyWormhole(pixels: IntArray, width: Int, height: Int) {
        val cx = width / 2
        val cy = height / 2
        for (y in 0 until height) {
            for (x in 0 until width) {
                val idx = y * width + x
                val dx = x - cx
                val dy = y - cy
                val dist = Math.sqrt((dx * dx + dy * dy).toDouble())
                val angle = Math.atan2(dy.toDouble(), dx.toDouble())
                val twist = angle + dist * 0.01
                val newX = (cx + dist * Math.cos(twist)).toInt().coerceIn(0, width - 1)
                val newY = (cy + dist * Math.sin(twist)).toInt().coerceIn(0, height - 1)
                pixels[idx] = temp[newY * width + newX]
            }
        }
    }

    private fun applyRobotEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val newR = 0
            val newG = gray
            val newB = gray
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyRobotVision(pixels: IntArray, width: Int, height: Int) {
        applyRobotEffect(pixels, width, height)
        for (y in 0 until height step 3) {
            for (x in 0 until width) {
                pixels[y * width + x] = Color.GREEN
            }
        }
    }

    private fun applyCyberpunkEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.8 + 50).toInt().coerceIn(0, 255)
            val newG = (g * 0.2).toInt().coerceIn(0, 255)
            val newB = (b * 1.2 + 80).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyCyberpunkHUD(pixels: IntArray, width: Int, height: Int) {
        applyCyberpunkEffect(pixels, width, height)
        for (y in 0 until height step 5) {
            for (x in 0 until width) {
                val alpha = Color.alpha(pixels[y * width + x])
                pixels[y * width + x] = Color.argb(alpha, 0, 255, 255)
            }
        }
    }

    private fun applyNeonVision(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val brightness = (r + g + b) / 3
            val newR = if (brightness > 128) 255 else 0
            val newG = if (brightness > 128) 0 else 255
            val newB = 255
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyHorrorEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val newR = (gray * 0.8).toInt().coerceIn(0, 255)
            val newG = (gray * 0.3).toInt().coerceIn(0, 255)
            val newB = (gray * 0.3).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyNightVision(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val newR = 0
            val newG = (gray * 1.5).toInt().coerceIn(0, 255)
            val newB = 0
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyThermalVision(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val temp = (r + g + b) / 3
            val newR = (temp * 2).toInt().coerceIn(0, 255)
            val newG = if (temp > 128) ((255 - temp) * 2).toInt() else 0
            val newB = if (temp < 128) ((128 - temp) * 2).toInt() else 0
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyXRayEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val gray = (r * 0.299 + g * 0.587 + b * 0.114).toInt()
            val newR = gray
            val newG = gray
            val newB = (gray * 1.2).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyInfraredEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 1.5).toInt().coerceIn(0, 255)
            val newG = 0
            val newB = 0
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyDigitalVision(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r / 16) * 16
            val newG = (g / 16) * 16
            val newB = (b / 16) * 16
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyMatrixVision(pixels: IntArray, width: Int, height: Int) {
        applyMatrixRain(pixels, width, height)
    }

    private fun applyGlitchVision(pixels: IntArray, width: Int, height: Int) {
        applyGlitch(pixels, width, height)
        for (i in pixels.indices) {
            if (Random.nextFloat() < 0.01f) {
                pixels[i] = Color.GREEN
            }
        }
    }

    private fun applyDreamVision(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 0.8 + 50).toInt().coerceIn(0, 255)
            val newG = (g * 0.6 + 80).toInt().coerceIn(0, 255)
            val newB = (b * 0.8 + 50).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyFutureVision(pixels: IntArray, width: Int, height: Int) {
        applyCyberpunkEffect(pixels, width, height)
    }

    private fun applyQuantumVision(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            if (Random.nextFloat() < 0.03f) {
                val hue = Random.nextFloat() * 360
                val hsv = floatArrayOf(hue, 1.0f, 1.0f)
                pixels[i] = Color.HSVToColor(hsv)
            }
        }
    }

    private fun applyCinematicEffect(pixels: IntArray, width: Int, height: Int) {
        val cx = width / 2.0
        val cy = height / 2.0
        val maxDist = Math.sqrt(cx * cx + cy * cy)
        for (y in 0 until height) {
            for (x in 0 until width) {
                val idx = y * width + x
                val dx = x - cx
                val dy = y - cy
                val dist = Math.sqrt(dx * dx + dy * dy)
                val vignette = (1.0 - dist / maxDist * 0.5).coerceIn(0.5, 1.0)
                val r = (Color.red(pixels[idx]) * vignette).toInt().coerceIn(0, 255)
                val g = (Color.green(pixels[idx]) * vignette).toInt().coerceIn(0, 255)
                val b = (Color.blue(pixels[idx]) * vignette).toInt().coerceIn(0, 255)
                pixels[idx] = Color.argb(Color.alpha(pixels[idx]), r, g, b)
            }
        }
    }

    private fun applySunsetEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 1.3 + 30).toInt().coerceIn(0, 255)
            val newG = (g * 0.7).toInt().coerceIn(0, 255)
            val newB = (b * 0.5).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyBeautyEffect(pixels: IntArray, width: Int, height: Int) {
        for (i in pixels.indices) {
            val r = Color.red(pixels[i])
            val g = Color.green(pixels[i])
            val b = Color.blue(pixels[i])
            val newR = (r * 1.1 + 10).toInt().coerceIn(0, 255)
            val newG = (g * 1.05 + 5).toInt().coerceIn(0, 255)
            val newB = (b * 1.1 + 10).toInt().coerceIn(0, 255)
            pixels[i] = Color.argb(Color.alpha(pixels[i]), newR, newG, newB)
        }
    }

    private fun applyFaceScanEffect(pixels: IntArray, width: Int, height: Int) {
        for (y in 0 until height) {
            if (y % 100 < 3) {
                for (x in 0 until width) {
                    pixels[y * width + x] = Color.GREEN
                }
            }
        }
    }

    private var temp = IntArray(0)
    private fun applyWormhole(pixels: IntArray, width: Int, height: Int) {
        temp = pixels.copyOf()
        val cx = width / 2
        val cy = height / 2
        for (y in 0 until height) {
            for (x in 0 until width) {
                val idx = y * width + x
                val dx = x - cx
                val dy = y - cy
                val dist = Math.sqrt((dx * dx + dy * dy).toDouble())
                val angle = Math.atan2(dy.toDouble(), dx.toDouble())
                val twist = angle + dist * 0.01
                val newX = (cx + dist * Math.cos(twist)).toInt().coerceIn(0, width - 1)
                val newY = (cy + dist * Math.sin(twist)).toInt().coerceIn(0, height - 1)
                pixels[idx] = temp[newY * width + newX]
            }
        }
    }
}
