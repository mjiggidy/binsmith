from setuptools import setup

setup(
	name="binsmith",
	version="2.0.0",
	packages=["binsmith"],
	install_requires=["pyavb==1.3.0"],
	entry_points={
		"console_scripts":[
			"binsmith = binsmith.__main__:bootstrap"
		]
	}
)