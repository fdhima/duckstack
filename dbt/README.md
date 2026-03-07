Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices


### Diagrams
Various architecture diagrams to help illustrate the workflow of the pipeline.

**Testing using dbt test**
The tests are performed at the project's startup (through `docker compose up`).
```mermaid
flowchart TD                                                                                                                                                                                
      A["dbt test"] --> B["Read dbt_project.yml"]                                                                                                                                             
      B --> C["Discover test sources"]                                                                                                                                                        
   
      C --> D["model-paths: models/"]                                                                                                                                                         
      C --> E["test-paths: tests/"]

      D --> F["Scan for schema.yml files in models/**"]
      E --> G["Scan for *.sql files in tests/"]

      F --> H["Parse generic tests per column definition"]
      G --> I["Load singular tests as raw SQL"]

      H --> J["Compile generic tests into SQL assertions e.g. SELECT count(*) WHERE col IS NULL"]
      I --> J

      J --> K["Execute all compiled SQL against DuckDB"]

      K --> L{Any rows returned or assertion fails?}
      L -- "No rows = PASS" --> M["Test PASSED"]
      L -- "Rows returned = FAIL" --> N["Test FAILED"]

      M --> O["Exit  pipeline continues"]
      N --> P["Exit  pipeline halts"]
```