from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from jobspy import scrape_jobs
import logging
import numpy as np
import pandas as pd

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI()

class JobSearchParams(BaseModel):
    job_sites: List[str]  # e.g., ["indeed", "linkedin"]
    job_title: str  # e.g., "Software Engineer"
    location: str  # e.g., "San Francisco, CA"
    is_remote: Optional[bool] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    job_type: Optional[str] = None  # e.g., "fulltime", "parttime"

@app.post("/scrape_jobs")
async def scrape_jobs_endpoint(params: JobSearchParams):
    try:
        # Log the received parameters for debugging
        logger.debug(f"Received job search parameters: {params}")

        # Build filters for salary if provided
        salary_filter = {}
        if params.min_salary is not None:
            salary_filter['min_amount'] = params.min_salary
        if params.max_salary is not None:
            salary_filter['max_amount'] = params.max_salary

        # Corrected proxy format with username and password
        proxies = [
            "ofpxsxmn:syjvmbnh6ivq@198.23.239.134:6540",
            "ofpxsxmn:syjvmbnh6ivq@107.172.163.27:6543",
            "ofpxsxmn:syjvmbnh6ivq@173.211.0.148:6641",
            "ofpxsxmn:syjvmbnh6ivq@167.160.180.203:6754",
            "ofpxsxmn:syjvmbnh6ivq@173.0.9.70:5653",
            "ofpxsxmn:syjvmbnh6ivq@173.0.9.209:5792"
        ]

        # Run job scraping based on parameters
        jobs = scrape_jobs(
            site_name=params.job_sites,
            search_term=params.job_title,
            location=params.location,
            is_remote=params.is_remote,
            job_type=params.job_type,
            results_wanted=20,  # Adjust based on preference
            **salary_filter,  # Unpack salary filters if present
            proxies=proxies
        )

        print(jobs)
        
        # Convert NaN and infinite values to None
        jobs = jobs.replace([np.nan, np.inf, -np.inf], None)

        # Convert to dictionary format for JSON response
        job_dict = jobs.to_dict(orient="records")
        
        print(job_dict)

        return {"jobs": job_dict}

    except Exception as e:
        logger.error("Error processing request:", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
