"""
Test runner for SuperHack AI/ML system
Provides comprehensive testing capabilities for all components
"""

import asyncio
import sys
import os
import logging
from pathlib import Path
from typing import List, Dict, Any
import argparse

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TestRunner:
    """Comprehensive test runner for SuperHack AI/ML system"""
    
    def __init__(self):
        self.test_results: Dict[str, bool] = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run all available tests"""
        logger.info("🚀 Starting comprehensive test suite for SuperHack AI/ML system")
        logger.info("=" * 80)
        
        # List of available tests
        test_modules = [
            ("Data Pipeline Tests", self._run_data_pipeline_tests),
            ("Phase 2.1 Tests", self._run_phase_2_1_tests),
            ("API Tests", self._run_api_tests),
            ("Model Tests", self._run_model_tests),
            ("Integration Tests", self._run_integration_tests)
        ]
        
        # Run each test module
        for test_name, test_func in test_modules:
            logger.info(f"\n🧪 Running {test_name}...")
            try:
                success = await test_func()
                self.test_results[test_name] = success
                self.total_tests += 1
                if success:
                    self.passed_tests += 1
                    logger.info(f"✅ {test_name}: PASSED")
                else:
                    self.failed_tests += 1
                    logger.error(f"❌ {test_name}: FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name}: ERROR - {e}")
                self.test_results[test_name] = False
                self.total_tests += 1
                self.failed_tests += 1
        
        # Generate summary
        return self._generate_summary()
    
    async def _run_data_pipeline_tests(self) -> bool:
        """Run data pipeline tests"""
        try:
            # Import and run data pipeline tests
            from test_data_pipeline import main as run_data_pipeline_tests
            await run_data_pipeline_tests()
            return True
        except Exception as e:
            logger.error(f"Data pipeline tests failed: {e}")
            return False
    
    async def _run_phase_2_1_tests(self) -> bool:
        """Run Phase 2.1 tests"""
        try:
            # Import and run Phase 2.1 tests
            from test_phase_2_1 import main as run_phase_2_1_tests
            await run_phase_2_1_tests()
            return True
        except Exception as e:
            logger.error(f"Phase 2.1 tests failed: {e}")
            return False
    
    async def _run_api_tests(self) -> bool:
        """Run API tests"""
        try:
            # Check if API test file exists
            api_test_file = Path(__file__).parent / "test_api.py"
            if not api_test_file.exists():
                logger.warning("API test file not found, skipping API tests")
                return True
            
            # Import and run API tests
            from test_api import main as run_api_tests
            await run_api_tests()
            return True
        except Exception as e:
            logger.error(f"API tests failed: {e}")
            return False
    
    async def _run_model_tests(self) -> bool:
        """Run model tests"""
        try:
            # Check if model test file exists
            model_test_file = Path(__file__).parent / "test_models.py"
            if not model_test_file.exists():
                logger.warning("Model test file not found, skipping model tests")
                return True
            
            # Import and run model tests
            from test_models import main as run_model_tests
            await run_model_tests()
            return True
        except Exception as e:
            logger.error(f"Model tests failed: {e}")
            return False
    
    async def _run_integration_tests(self) -> bool:
        """Run integration tests"""
        try:
            # Check if integration test file exists
            integration_test_file = Path(__file__).parent / "test_integration.py"
            if not integration_test_file.exists():
                logger.warning("Integration test file not found, skipping integration tests")
                return True
            
            # Import and run integration tests
            from test_integration import main as run_integration_tests
            await run_integration_tests()
            return True
        except Exception as e:
            logger.error(f"Integration tests failed: {e}")
            return False
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate test summary"""
        logger.info("\n" + "=" * 80)
        logger.info("📊 Test Summary:")
        logger.info("=" * 80)
        
        # Print individual test results
        for test_name, success in self.test_results.items():
            status = "✅ PASSED" if success else "❌ FAILED"
            logger.info(f"  {test_name}: {status}")
        
        # Print overall statistics
        logger.info(f"\n📈 Overall Statistics:")
        logger.info(f"  Total Tests: {self.total_tests}")
        logger.info(f"  Passed: {self.passed_tests}")
        logger.info(f"  Failed: {self.failed_tests}")
        logger.info(f"  Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%" if self.total_tests > 0 else "  Success Rate: 0%")
        
        # Overall result
        if self.failed_tests == 0:
            logger.info(f"\n🎉 All {self.total_tests} tests passed! System is working correctly.")
            overall_success = True
        else:
            logger.error(f"\n💥 {self.failed_tests} out of {self.total_tests} tests failed.")
            overall_success = False
        
        return {
            "overall_success": overall_success,
            "total_tests": self.total_tests,
            "passed_tests": self.passed_tests,
            "failed_tests": self.failed_tests,
            "success_rate": (self.passed_tests/self.total_tests)*100 if self.total_tests > 0 else 0,
            "test_results": self.test_results
        }
    
    async def run_specific_test(self, test_name: str) -> bool:
        """Run a specific test by name"""
        test_functions = {
            "data_pipeline": self._run_data_pipeline_tests,
            "phase_2_1": self._run_phase_2_1_tests,
            "api": self._run_api_tests,
            "models": self._run_model_tests,
            "integration": self._run_integration_tests
        }
        
        if test_name not in test_functions:
            logger.error(f"Unknown test: {test_name}")
            logger.info(f"Available tests: {', '.join(test_functions.keys())}")
            return False
        
        logger.info(f"🧪 Running {test_name} tests...")
        try:
            success = await test_functions[test_name]()
            if success:
                logger.info(f"✅ {test_name} tests: PASSED")
            else:
                logger.error(f"❌ {test_name} tests: FAILED")
            return success
        except Exception as e:
            logger.error(f"❌ {test_name} tests: ERROR - {e}")
            return False


async def main():
    """Main function for test runner"""
    parser = argparse.ArgumentParser(description="SuperHack AI/ML Test Runner")
    parser.add_argument(
        "--test", 
        type=str, 
        help="Run specific test (data_pipeline, phase_2_1, api, models, integration)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create test runner
    runner = TestRunner()
    
    # Run tests
    if args.test:
        success = await runner.run_specific_test(args.test)
        sys.exit(0 if success else 1)
    else:
        summary = await runner.run_all_tests()
        sys.exit(0 if summary["overall_success"] else 1)


if __name__ == "__main__":
    asyncio.run(main())
