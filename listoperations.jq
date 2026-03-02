# listoperations.jq

# 1 - Selects paths objects and filters out x-tensions
#----------------------------------------------------
# Use with_entries to select paths that don't start with "x-"
.paths
| with_entries(select(.key | test("^x-") | not))

# 2 - Creates an array of operations
#-----------------------------------
# returns [{path, method, summary, deprecated}]
| to_entries # Start processing paths as key/value pairs
| map ( # Applies a transformation to each element (path)
  .key as $path # Stores the path value
  | .value
  | to_entries # Transforms { "get": {...} } to [ { "key": "get", "value": {...} } ]
  | map( # Applies a transformation to each element (method)
    select( # Keeps only standard HTTP verbs
      .key | IN("get", "put", "post", "delete",
           "options", "head", "patch", "trace")
    )
    | # Creates a new JSON object
    {
      method: .key,
      path: $path, 
      summary: (.value.summary? // ""),
      deprecated: .value.deprecated?
    }
  )[] # Flattens array
) # Now we have an array of {path, method, summary, deprecated}

# 3 - Outputs tab separated raw text (using string interpolation)
#-----------------------------------
| map( # Applies a transformation to each element
  "\( (.method | ascii_upcase) )\t\(.path)\t\(.summary)\(if .deprecated then " (deprecated)" else "" end)"
)
[] # Flattens array for raw output
