"""High-level translation orchestration."""

from __future__ import annotations

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

