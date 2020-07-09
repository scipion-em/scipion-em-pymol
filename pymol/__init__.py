# **************************************************************************
# *
# * Authors:     David Herreros Calero (dherreros@cnb.csic.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import pwem
from .constants import PYMOL_HOME, V2_4_0

_logo = "icon.png"
_references = ['you2019']


class Plugin(pwem.Plugin):
    _homeVar = PYMOL_HOME
    _pathVars = [PYMOL_HOME]
    _supportedVersions = [V2_4_0]

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(PYMOL_HOME, 'pymol-' + cls.getActiveVersion())

    @classmethod
    def isVersion(cls, version='2.4.0'):
        return cls.getActiveVersion().startswith(version)

    @classmethod
    def getPymolActivation(cls):
        return "conda activate pymol" + cls.getActiveVersion()

    @classmethod
    def runPymolScript(cls, protocol, script):
        pymolCall = '%s %s && %s/pymol-build/bin/pymol -cq' % (cls.getCondaActivationCmd(),
                                                               cls.getPymolActivation(), cls.getHome())
        protocol.runJob(pymolCall, script)

    @classmethod
    def defineBinaries(cls, env):
        SW_EM = env.getEmFolder()

        installationCmd = cls.getCondaActivationCmd()
        installationCmd += 'conda create -y -n pymol%s python=3.7 && ' % V2_4_0
        installationCmd += 'conda activate pymol%s && ' % V2_4_0
        installationCmd += 'conda install -c anaconda pyqt -y && conda install -c conda-forge pmw -y && '
        installationCmd += 'conda install -c openbabel openbabel -y && '
        installationCmd += 'cd .. && wget -N https://github.com/rcsb/mmtf-cpp/archive/7c74b18.tar.gz && '
        installationCmd += 'tar -xf 7c74b18.tar.gz && mv pymol-open-source-95a44ada8bacfe345905a5df0a70376eb1b455b1 pymol && '
        installationCmd += 'mv mmtf-cpp*/include/mmtf* pymol/include/ && '
        installationCmd += 'cd pymol && python setup.py build install --home=%s/pymol/pymol-build && ' % SW_EM
        installationCmd += 'touch pymol_installed'
        pymol240_commands = [(installationCmd, "%s/pymol/pymol_installed" % SW_EM)]


        env.addPackage('pymol', version=V2_4_0,
                       url='https://github.com/schrodinger/pymol-open-source/archive/95a44ad.tar.gz',
                       buildDir='pymol-open-source-95a44ada8bacfe345905a5df0a70376eb1b455b1',
                       commands=pymol240_commands,
                       targetDir='pymol',
                       default=True)
