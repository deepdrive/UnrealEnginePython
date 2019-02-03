#!/usr/bin/env python3
from ue4helpers import ConanUtils, FilesystemUtils, PlatformInfo, PluginPackager, SubprocessUtils, VersionHelpers
from os.path import abspath, dirname, join

# Build a UE4-compatible version of CPython 3.6.8
print('Building our embeddable Python distribution...')
SubprocessUtils.run(['ue4', 'conan', 'update'])
SubprocessUtils.run(['ue4', 'conan', 'build', 'python-ue4==3.6.8'])

# Bundle the custom-built Python distribution in our source tree
print('Bundling our embeddable Python distribution...')
root = dirname(dirname(abspath(__file__)))
bundled = join(root, 'EmbeddedPython', PlatformInfo.identifier())
ConanUtils.copy_package('python-ue4/3.6.8@adamrehn/4.21', bundled)

# Create our plugin packager
packager = PluginPackager(
	root = root,
	version = VersionHelpers.from_git_commit(),
	archive = '{name}-{version}-{platform}'
)

# Clean any previous build artifacts
packager.clean()

# Package the plugin
packager.package()

# Compress the packaged distribution
archive = packager.archive()

# TODO: upload the archive to Amazon S3
print('Created compressed archive "{}".'.format(archive))
