package main

import (
	"flag"
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
)

func main() {
	searchFilter := flag.String("filter", "", "Instance filter string")
	flag.Parse()
	sess := session.Must(session.NewSessionWithOptions(session.Options{
		SharedConfigState: session.SharedConfigEnable,
	}))

	svc := ec2.New(sess)

	paramsInput := &ec2.DescribeInstancesInput{
		Filters: []*ec2.Filter{
			&ec2.Filter{
				Name: aws.String(*searchFilter),
				Values: []*string{
					aws.String("owned"),
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
		fmt.Println("Total number of instances:", len(result.Reservations), ",filtered by:", *searchFilter)
	}
}
