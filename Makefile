# Makefile for lybic-python-sdk
#
# Copyright (c) 2019-2025   Beijing Tingyu Technology Co., Ltd.
# Copyright (c) 2025        Lybic Development Team <team@lybic.ai, lybic@tingyutech.com>
# Copyright (c) 2025        Lu Yicheng <luyicheng@tingyutech.com>
#
# Author: AEnjoy <aenjoyable@163.com>
#
# These Terms of Service ("Terms") set forth the rules governing your access to and use of the website lybic.ai
# ("Website"), our web applications, and other services (collectively, the "Services") provided by Beijing Tingyu
# Technology Co., Ltd. ("Company," "we," "us," or "our"), a company registered in Haidian District, Beijing. Any
# breach of these Terms may result in the suspension or termination of your access to the Services.
# By accessing and using the Services and/or the Website, you represent that you are at least 18 years old,
# acknowledge that you have read and understood these Terms, and agree to be bound by them. By using or accessing
# the Services and/or the Website, you further represent and warrant that you have the legal capacity and authority
# to agree to these Terms, whether as an individual or on behalf of a company. If you do not agree to all of these
# Terms, do not access or use the Website or Services.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
.PHONY: help build publish clean clean-build-cache clean-venv create-venv

# Variables
PYTHON := python3
VENV_DIR := .venv

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  help               Display this help message"
	@echo "  create-venv        Create a virtual environment in .venv/"
	@echo "  build              Build the python package"
	@echo "  publish            Publish the package to PyPI"
	@echo "  test-[e2e]         Execute the [e2e] tests"
	@echo "  clean              Remove build artifacts"
	@echo "  clean-build-cache  Remove Python cache files"
	@echo "  clean-venv         Remove the virtual environment"


create-venv:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	@echo "Virtual environment created in $(VENV_DIR)"
	@echo "To activate, run: source $(VENV_DIR)/bin/activate"

build:
	@echo "Building the package..."
	$(PYTHON) -m build

publish:
	@echo "Publishing the package..."
	twine upload dist/*

test-e2e:
	@echo "Running end-to-end tests..."
	LYBIC_ORG_ID=test LYBIC_API_KEY=test LYBIC_API_ENDPOINT=http://localhost:4010 $(PYTHON) -m test.e2e

clean: clean-build-cache
	@echo "Cleaning build artifacts..."
	rm -rf build dist *.egg-info

clean-build-cache:
	@echo "Cleaning Python cache files..."
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean-venv:
	@echo "Removing virtual environment..."
	rm -rf $(VENV_DIR)
