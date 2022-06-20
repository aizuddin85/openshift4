package main

import (
	"flag"
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
)

func main() {
	searchFilterKey := flag.String("filterKey", "", "Instance tag filter key")
	searchFilterVal := flag.String("filterVal", "", "Instance tag filter value")
	flag.Parse()

	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	svc := ec2.New(sess)

	paramsInput := &ec2.DescribeInstancesInput{
		Filters: []*ec2.Filter{
			&ec2.Filter{
				Name: aws.String(*searchFilterKey),
				Values: []*string{
					aws.String(*searchFilterVal),
				},
			},
		},
	}

	result, err := svc.DescribeInstances(paramsInput)

	if err != nil {
		fmt.Println(err)
	} else {
		for idx, _ := range result.Reservations {
			for _, inst := range result.Reservations[idx].Instances {
				fmt.Println("	--------------------------")
				for _, tag := range inst.Tags {
					if *tag.Key == "Name" {
						fmt.Println("    - Instance ID:       ", *inst.InstanceId)
						fmt.Println("      Instance Name:     ", *tag.Value)
						fmt.Println("      Instance State:    ", *inst.State.Name)
						fmt.Println("      Instance Location: ", *inst.Placement.AvailabilityZone)
					}
				}
			}
		}
		fmt.Println("Total number of instances:", len(result.Reservations), ",filtered by:", *searchFilterKey)
	}
}
