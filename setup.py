


from setuptools import setup, find_packages
if __name__ == '__main__':
    setup(
        name='exporter',
        version="0.1",
        description="Ictp Custom data exporter",
        author="Giorgio Pieretti",
        packages=find_packages(),
        include_package_data=True,
        package_dir={'exporter': 'exporter'},
        entry_points="""
            [indico.ext_types]
            exporter = indico.ext.exporter
            
            [indico.ext]
            exporter.ictp = indico.ext.exporter.ictp
        """
    )