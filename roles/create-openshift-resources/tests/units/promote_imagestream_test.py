import sys
import subprocess
import pytest

import promote_imagestream


class TestClass:

    @pytest.mark.skip()
    def test_service_account_should_not_exist(self):
        # given nothing

        # when
        result = promote_imagestream.does_service_account_exist('test-sa', 'python-tests-build')
        # then
        assert result is False

    @pytest.mark.skip()
    def test_service_account_should_exist_with_role(self):
        # given
        promote_imagestream.create_service_account('test-sa', 'python-tests-build')
        promote_imagestream.add_role_to_user('edit', 'test-sa', 'python-tests-build')

        # when
        result = promote_imagestream.does_service_account_exist('test-sa', 'python-tests-build')
        # then
        assert result is True
        # cleanup
        promote_imagestream.delete_service_account('test-sa', 'python-tests-build')

    def test_should_promote_image(self):
        # given
        # example app created in setup

        # when
        promote_imagestream.promote_image_when_available('python-tests-build', 'nodejs-mongodb-example', 'latest', 'python-tests-promote')

        # then
        assert promote_imagestream.does_imagestream_tag_exist('nodejs-mongodb-example', 'latest', 'python-tests-promote') is True

    def test_should_fail_because_src_imagestream_is_missing(self):
        # given

        # when
        try:
            promote_imagestream.promote_image_when_available('python-tests-build', 'missing-imagestream', 'latest', 'python-tests-promote')
            assert False, "Exception should have been raised already"
        except subprocess.CalledProcessError as e:
            # then
            assert "missing-imagestream" in e.output

    def test_should_fail_because_src_project_is_missing(self):
        # given

        # when
        try:
            promote_imagestream.promote_image_when_available('missing-source-project', 'nodejs-mongodb-example', 'latest', 'python-tests-promote')
            assert False, "Exception should have been raised already"
        except subprocess.CalledProcessError as e:
            # then
            assert "missing-source-project" in e.output

    def test_should_fail_because_dst_project_is_missing(self):
        # given

        # when
        try:
            promote_imagestream.promote_image_when_available('python-tests-build', 'nodejs-mongodb-example', 'latest', 'missing-destination-project')
            assert False, "Exception should have been raised already"
        except subprocess.CalledProcessError as e:
            # then
            assert "missing-destination-project" in e.output

    @classmethod
    def setup_class(cls):
        promote_imagestream.create_openshift_project('python-tests-build')
        promote_imagestream.create_nodejs_example_app('python-tests-build')
        promote_imagestream.create_openshift_project('python-tests-promote')

    @classmethod
    def teardown_class(cls):
        promote_imagestream.delete_openshift_project('python-tests-build')
        promote_imagestream.delete_openshift_project('python-tests-promote')
