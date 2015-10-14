from . import VMBaseClass
from unittest import TestCase

import textwrap
import os


class TestLvmAbs(VMBaseClass, TestCase):
    __test__ = False
    conf_file = "examples/tests/lvm.yaml"
    install_timeout = 600
    boot_timeout = 100
    interactive = False
    extra_disks = []
    collect_scripts = [textwrap.dedent("""
        cd OUTPUT_COLLECT_D
        cat /etc/fstab > fstab
        ls /dev/disk/by-dname > ls_dname
        pvdisplay -C --separator = -o vg_name,pv_name --noheadings > pvs
        lvdisplay -C --separator = -o lv_name,vg_name --noheadings > lvs
        """)]

    def test_fstab(self):
        with open(os.path.join(self.td.mnt, "fstab")) as fp:
            fstab_lines = fp.readlines()
        fstab_entry = None
        for line in fstab_lines:
            if "/dev/vg1/lv1" in line:
                fstab_entry = line
                self.assertIsNotNone(fstab_entry)
                self.assertEqual(fstab_entry.split(' ')[1], "/srv/data")
            if "/dev/vg1/lv2" in line:
                fstab_entry = line
                self.assertIsNotNone(fstab_entry)
                self.assertEqual(fstab_entry.split(' ')[1], "/srv/backup")

    def test_lvs(self):
        with open(os.path.join(self.td.mnt, "lvs"), "r") as fp:
            lv_data = list(i.strip() for i in fp.readlines())
        self.assertIn("lv1=vg1", lv_data)
        self.assertIn("lv2=vg1", lv_data)

    def test_pvs(self):
        with open(os.path.join(self.td.mnt, "pvs"), "r") as fp:
            lv_data = list(i.strip() for i in fp.readlines())
        self.assertIn("vg1=/dev/vda5", lv_data)
        self.assertIn("vg1=/dev/vda6", lv_data)

    def test_output_files_exist(self):
        self.output_files_exist(
            ["fstab", "ls_dname"])

    def test_dname(self):
        with open(os.path.join(self.td.mnt, "ls_dname"), "r") as fp:
            contents = fp.read().splitlines()
        for link in list(("main_disk-part%s" % i for i in (1, 5, 6))):
            self.assertIn(link, contents)
        self.assertIn("main_disk", contents)
        self.assertIn("vg1-lv1", contents)
        self.assertIn("vg1-lv2", contents)


class WilyTestLvm(TestLvmAbs):
    __test__ = True
    repo = "maas-daily"
    release = "wily"
    arch = "amd64"


class VividTestLvm(TestLvmAbs):
    __test__ = True
    repo = "maas-daily"
    release = "vivid"
    arch = "amd64"
