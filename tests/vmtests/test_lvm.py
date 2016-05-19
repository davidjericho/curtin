from . import VMBaseClass
from .releases import base_vm_classes as relbase

import textwrap


class TestLvmAbs(VMBaseClass):
    conf_file = "examples/tests/lvm.yaml"
    interactive = False
    extra_disks = []
    collect_scripts = [textwrap.dedent("""
        cd OUTPUT_COLLECT_D
        cat /etc/fstab > fstab
        ls /dev/disk/by-dname > ls_dname
        pvdisplay -C --separator = -o vg_name,pv_name --noheadings > pvs
        lvdisplay -C --separator = -o lv_name,vg_name --noheadings > lvs
        """)]
    fstab_expected = {
        '/dev/vg1/lv1': '/srv/data',
        '/dev/vg1/lv2': '/srv/backup',
    }
    disk_to_check = [('main_disk', 1),
                     ('main_disk', 5),
                     ('main_disk', 6),
                     ('vg1-lv1', 0),
                     ('vg1-lv2', 0)]

    def test_lvs(self):
        self.check_file_strippedline("lvs", "lv1=vg1")
        self.check_file_strippedline("lvs", "lv2=vg1")

    def test_pvs(self):
        self.check_file_strippedline("pvs", "vg1=/dev/vda5")
        self.check_file_strippedline("pvs", "vg1=/dev/vda6")

    def test_output_files_exist(self):
        self.output_files_exist(
            ["fstab", "ls_dname"])


class PreciseTestLvm(relbase.precise, TestLvmAbs):
    __test__ = True

    # FIXME(LP: #1523037): dname does not work on trusty, so we cannot expect
    # sda-part2 to exist in /dev/disk/by-dname as we can on other releases
    # when dname works on trusty, then we need to re-enable by removing line.
    def test_dname(self):
        print("test_dname does not work for Trusty")


class PreciseHWETTestLvm(relbase.precise_hwe_t, PreciseTestLvm):
    __test__ = True


class TrustyTestLvm(relbase.trusty, TestLvmAbs):
    __test__ = True

    # FIXME(LP: #1523037): dname does not work on trusty, so we cannot expect
    # sda-part2 to exist in /dev/disk/by-dname as we can on other releases
    # when dname works on trusty, then we need to re-enable by removing line.
    def test_dname(self):
        print("test_dname does not work for Trusty")


class VividTestLvm(relbase.vivid, TestLvmAbs):
    __test__ = True


class WilyTestLvm(relbase.wily, TestLvmAbs):
    __test__ = True


class XenialTestLvm(relbase.xenial, TestLvmAbs):
    __test__ = True
