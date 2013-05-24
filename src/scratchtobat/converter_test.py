from __future__ import unicode_literals

import unittest
import org.catrobat.catroid.common as catcommon
import org.catrobat.catroid.content as catbase
import org.catrobat.catroid.content.bricks as catbricks
import org.catrobat.catroid.io as catio
import org.catrobat.catroid.formulaeditor as catformula
from scratchtobat import sb2_test, converter, sb2, common, testing_common, \
    catrobat
from java.lang import System


DUMMY_CATR_SPRITE = catbase.Sprite("Dummy")
TEST_PROJECT = sb2.Project(testing_common.get_test_project_path("dancing_castle"))


class TestConvertExampleProject(testing_common.ScratchtobatTestCase):
    
    dummy_sb2_object = sb2.Object({"objName" : "Dummy"})
    
    expected_sprite_names = ["Sprite1, Cassy Dance"]
    expected_script_classes = [[catbase.StartScript, ], []]
    expected_brick_classes = [[catbricks.WaitBrick, catbricks.RepeatBrick, catbricks.MoveNStepsBrick, catbricks.WaitBrick, catbricks.MoveNStepsBrick,
            catbricks.WaitBrick, catbricks.LoopEndBrick], []]
    
    def __init__(self, methodName='runTest'):
        testing_common.ScratchtobatTestCase.__init__(self, methodName=methodName)
        assert System.getProperty("python.security.respectJavaAccessibility") == 'false', "Jython registry property 'python.security.respectJavaAccessibility' must be set to 'false'"
    
    def setUp(self):
        self.project = TEST_PROJECT
        
    def test_can_convert_complete_project_to_catrobat_project_class(self):
        catr_project = converter.convert_to_catrobat_project(self.project)
        self.assertTrue(isinstance(catr_project, catbase.Project), "Converted project is not a catroid project class.")
        
        catr_sprites = catr_project.getSpriteList()
        self.assertTrue(catr_sprites, "No sprites in converted project.")
        self.assertTrue(all(isinstance(_, catbase.Sprite) for _ in catr_sprites), "Sprites of converted project are not catroid sprite classes.")
        
    def test_can_convert_object_to_catrobat_sprite_class(self):
        sprites = [converter._convert_to_catrobat_sprite(sb2obj) for sb2obj in self.project.objects]
        self.assertTrue(all(isinstance(_, catbase.Sprite) for _ in sprites))
        
        sprite_0 = sprites[0] 
        self.assertEqual("Stage", sprite_0.getName())
        # FIXME: add implicit script and brick
#         self.assertEqual(1, sprite_0.getNumberOfScripts())
#         self.assertEqual(1, sprite_0.getNumberOfBricks())
        sprite0_looks = sprite_0.getLookDataList()
        self.assertTrue(sprite0_looks, "No looks in sprite1")
        self.assertTrue(all(isinstance(_, catcommon.LookData) for _ in sprite0_looks), "Wrong classes in look list1")
        sprite0_sounds = sprite_0.getSoundList()
        self.assertTrue(sprite0_sounds, "No sounds in sprite1")
        self.assertTrue(all(isinstance(_, catcommon.SoundInfo) for _ in sprite0_sounds), "Wrong classes in sound list1")
        
        sprite_1 = sprites[1]
        self.assertEqual("Sprite1", sprite_1.getName())
        # FIXME: add implicit script and brick
        self.assertEqual(2, sprite_1.getNumberOfScripts())
        self.assertEqual(8, sprite_1.getNumberOfBricks())
        sprite1_looks = sprite_1.getLookDataList()
        self.assertTrue(sprite1_looks, "No looks in sprite1")
        self.assertTrue(all(isinstance(_, catcommon.LookData) for _ in sprite1_looks), "Wrong classes in look list1")
        sprite1_sounds = sprite_1.getSoundList()
        self.assertTrue(sprite1_sounds, "No sounds in sprite1")
        self.assertTrue(all(isinstance(_, catcommon.SoundInfo) for _ in sprite1_sounds), "Wrong classes in sound list1")
        
        sprite_2 = sprites[2]
        self.assertEqual("Cassy Dance", sprite_2.getName())
        # FIXME: add implicit script and brick
        self.assertEqual(1, sprite_2.getNumberOfScripts())
        self.assertEqual(5, sprite_2.getNumberOfBricks())
        sprite2_looks = sprite_2.getLookDataList()
        self.assertTrue(sprite2_looks, "No looks in sprite2")
        self.assertTrue(all(isinstance(_, catcommon.LookData) for _ in sprite2_looks), "Wrong classes in look list2")

    def test_can_convert_script_to_catrobat_script_class(self):
        sb2_script = self.project.objects[1].scripts[0]
        catr_script = converter._convert_to_catrobat_script(sb2_script, DUMMY_CATR_SPRITE)
        self.assertTrue(catr_script, "No script from conversion")
        expected_script_class = [catbase.StartScript]
        expected_brick_classes = [catbricks.WaitBrick, catbricks.RepeatBrick, catbricks.MoveNStepsBrick, catbricks.WaitBrick, catbricks.MoveNStepsBrick,
            catbricks.WaitBrick, catbricks.LoopEndBrick]
        self.assertScriptClasses(expected_script_class, expected_brick_classes, catr_script)
    
    def test_can_convert_costume_to_catrobat_lookdata_class(self):
        costumes = self.project.objects[1].get_costumes()
        for expected_values, costume in zip([("costume1", "f9a1c175dbe2e5dee472858dd30d16bb_costume1.svg"),
                ("costume2", "6e8bd9ae68fdb02b7e1e3df656a75635_costume2.svg")], costumes):
            look = converter._convert_to_catrobat_look(costume) 
            self.assertTrue(isinstance(look, catcommon.LookData), "Costume conversion return wrong class")
            self.assertEqual(look.getLookName(), expected_values[0], "Look name wrong")
            self.assertEqual(look.getLookFileName(), expected_values[1], "Look file name wrong")
        
    def test_can_convert_sound_to_catrobat_soundinfo_class(self):
        sounds = self.project.objects[1].get_sounds()
        for expected_values, sound in zip([("meow", "83c36d806dc92327b9e7049a565c6bff_meow.wav"), ], sounds):
            soundinfo = converter._convert_to_catrobat_sound(sound) 
            self.assertTrue(isinstance(soundinfo, catcommon.SoundInfo), "Sound conversion return wrong class")
            self.assertEqual(soundinfo.getTitle(), expected_values[0], "Sound name wrong")
            self.assertEqual(soundinfo.getSoundFileName(), expected_values[1], "Sound file name wrong")
    
    def test_can_write_sb2_project_to_catrobat_xml(self):
        catr_project = converter.convert_to_catrobat_project(self.project)
        common.log.info(catio.StorageHandler.getInstance().getXMLStringOfAProject(catr_project))        


class TestConvertBricks(unittest.TestCase):
    
    def get_sprite_with_soundinfo(self, soundinfo_name):
        dummy_sound = catcommon.SoundInfo()
        dummy_sound.setTitle(soundinfo_name)
        dummy_sprite = catbase.Sprite("TestDummy")
        dummy_sprite.getSoundList().add(dummy_sound)
        return dummy_sprite
    
    def test_fail_on_unknown_brick(self):
        with self.assertRaises(common.ScratchtobatError):
            converter._convert_to_catrobat_bricks(['wrong_brick_name_zzz', 10, 10], DUMMY_CATR_SPRITE)
    
    def test_can_convert_loop_bricks(self):
        sb2_do_loop = ["doRepeat", 10, [[u'forward:', 10], [u'playDrum', 1, 0.2], [u'forward:', -10], [u'playDrum', 1, 0.2]]]
        catr_do_loop = converter._convert_to_catrobat_bricks(sb2_do_loop, DUMMY_CATR_SPRITE)
        self.assertTrue(isinstance(catr_do_loop, list))
        # 1 loop start + 4 inner loop bricks + 1 loop end = 6
        self.assertEqual(6, len(catr_do_loop))
        expected_brick_classes = [catbricks.RepeatBrick, catbricks.MoveNStepsBrick, catbricks.WaitBrick, catbricks.MoveNStepsBrick,
            catbricks.WaitBrick, catbricks.LoopEndBrick]
        self.assertEqual(expected_brick_classes, [_.__class__ for _ in catr_do_loop])

    def test_can_convert_waitelapsedfrom_brick(self):
        sb2_brick = ["wait:elapsed:from:", 1]
        [catr_brick] = converter._convert_to_catrobat_bricks(sb2_brick, DUMMY_CATR_SPRITE)
        self.assertTrue(isinstance(catr_brick, catbricks.WaitBrick))
        self.assertTrue(catrobat.compare_formulas(catr_brick.timeToWaitInSeconds, catformula.Formula(1.0 / 1000)))

    def test_fail_convert_playsound_brick_if_sound_missing(self):
        sb2_brick = ["playSound:", "bird"]
        with self.assertRaises(converter.ConversionError):
            converter._convert_to_catrobat_bricks(sb2_brick, DUMMY_CATR_SPRITE)
    
    def test_can_convert_playsound_brick(self):
        sb2_brick = ["playSound:", "bird"]
        dummy_sprite = self.get_sprite_with_soundinfo(sb2_brick[1])
        [catr_brick] = converter._convert_to_catrobat_bricks(sb2_brick, dummy_sprite)
        self.assertTrue(isinstance(catr_brick, catbricks.PlaySoundBrick))
        self.assertEqual(sb2_brick[1], catr_brick.sound.getTitle())
        
    def test_can_convert_nextcostume_brick(self):
        sb2_brick = ["nextCostume"]
        [catr_brick] = converter._convert_to_catrobat_bricks(sb2_brick, DUMMY_CATR_SPRITE)
        self.assertTrue(isinstance(catr_brick, catbricks.NextLookBrick))

if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
