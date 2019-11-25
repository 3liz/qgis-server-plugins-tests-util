# Plugins tests setup

This is a "standard" set up for running tests for Qgis server plugins.

This setup run tests inside a QGIS platform Docker container: https://hub.docker.com/r/3liz/qgis-platform,
so you can choose the version of the platform to test your plugin against.

The test use a image named `qgis_platform:<whatever_version>`, if you pull an image from the 3liz
repository on dockerhub you will have to  retag it from `3liz/qgis_platform:XXX` to `qgis_platform:XXX` or
define the variable `REGISTRY_URL=3liz` when running tests.
``` tests

## Running your tests

From the root of your  repository run:

```bash
docker pull 3liz/qgis-platform:3.4
docker tag 3liz/qgis-platform:3.4 qgis-platform:3.4
make -C tests
```

Remember that your can put your folder test anywhere but changes the Makefile accordingly.

## Install test suite in your repository

This is a suggestion for organizing your plugin source repository, you can
choose a different organization but in this case change paths in Makefile accordingly.

In the default configuration, the repository is expected to organized as follow:

```
<your_repository>
├── myplugin/
│   ├── __init__.py
│   ├── metadata.txt
│   └── ...
├── .lizcloud/
|       ├── fabric.mk
|       ├── factory.mk
|       ├── metadata_key
└── tests
     ├── Makefile
     ├── conftest.py
     ├── pytest.ini
     ├── requirements.txt
     ├── run-tests.sh
     ├── data/PUT_YOUR_TEST_DATE_HERE
     └── ...PUT_YOUR_TESTS_HERE
```

## Create your tests

The tests framework is [pytest](https://pytest.org/en/latest/) and is compatible with `unittests`.

### Fixtures 

#### `client` fixture

The `client` fixture is a session defined fixture that create a QgsServer object far testing requests.

Example:

```python
def test_getcapabilitiesatlas(client):
    """  Test getcapabilites response
    """
    projectfile = "data/france_parts.qgs"

    # Make a request
    #
    # The MAP parameter is not required as a QgsProject will be created 
    # and passed to the request object.
    # Some plugins may request this parameters
    # but they should use the 'QgsServerInterface.configFilePath()' method
    # to get the real path of the project

    qs = "?SERVICE=WMS&REQUEST=GetCapabilitiesAtlas&MAP=data/france_parts.qgs"
    rv = client.get(qs, projectfile)
    assert rv.status_code == 200

```

The `get()` method will return an `OWSResponse` object:

```python
class OWSResponse:

    @property
    def xml(self) -> 'xml':
        """ Return the response as an lxml etree object 

            The returned body must be an XML response
        """

    @property
    def content(self) -> bytes:
        """ Return the raw body of the request """

    @property
    def status_code(self) -> int:
        """ Return the status code of the request """ 

    @property
    def headers(self) -> Dict[str,str]:
        """ Return the response headers """

    def xpath(self, path: str) -> lxml.etree.Element:
        """ Return at lxml etree element """

    def xpath_text(self, path: str) -> str:
        """ Return the text part of a lxml etree element """

```

### Access your plugins modules

#### As python module

Unit tests will require that you access the plugin as  module. The plugin is loaded by the client and
put in the global namespace, so you may access plugins methods like any other python module.

```python
def test_myplugin(client):

    import myPluginDirName
    ...
```

#### From the `client` interface

You may get the plugin module object with the `client.getplugin()` method: this method 
will return the object return by the `serverClassFactory` plugin method.

```python
def test_myplugin( client ):

    # Access the plugin object returned by the 'serverClassFactory' function.

    plugin = client.getplugin('myPluginName') 
    ...
``` 
